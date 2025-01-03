import subprocess
from prettytable import PrettyTable

class PingChecker:
    def __init__(self, input_file):
        self.input_file = input_file
        self.targets = self.load_targets()
        self.pinged_targets = []
        self.no_ping_targets = []

    def load_targets(self):
        """Carga los objetivos desde el archivo de texto."""
        with open(self.input_file, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def ping(self, target):
        """Realiza un ping a un objetivo y retorna True si responde."""
        command = ['ping', '-c', '1', target]  # '-c 1' para Linux/Unix; usar '-n 1' en Windows
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_targets(self):
        """Verifica cada objetivo y clasifica según la respuesta."""
        for target in self.targets:
            if self.ping(target):
                self.pinged_targets.append(target)
            else:
                self.no_ping_targets.append(target)

    def save_results(self):
        """Guarda los resultados en archivos de texto."""
        with open('targetsPing.txt', 'w') as ping_file:
            ping_file.write("\n".join(self.pinged_targets))
        
        with open('targetsNoPing.txt', 'w') as no_ping_file:
            no_ping_file.write("\n".join(self.no_ping_targets))

    def display_results(self):
        """Muestra los resultados en forma de tabla y mensajes informativos."""
        # Tabla para objetivos que hacen ping
        table_ping = PrettyTable()
        table_ping.field_names = ["Objetivos que hacen Ping"]
        for target in self.pinged_targets:
            table_ping.add_row([target])
        
        # Tabla para objetivos que no hacen ping
        table_no_ping = PrettyTable()
        table_no_ping.field_names = ["Objetivos que NO hacen Ping"]
        for target in self.no_ping_targets:
            table_no_ping.add_row([target])

        print(table_ping)
        print(f"\nHay un total de {len(self.pinged_targets)} objetivos que hacen ping y se encuentran almacenados en 'targetsPing.txt'.")
        
        print(table_no_ping)
        print(f"\nHay un total de {len(self.no_ping_targets)} objetivos que NO hacen ping y se encuentran almacenados en 'targetsNoPing.txt'.")

def main():
    checker = PingChecker('targets.txt')
    checker.check_targets()
    checker.save_results()
    checker.display_results()

if __name__ == "__main__":
    main()
