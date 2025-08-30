from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Este comando ejecuta todos los comandos de seeding del gamecenter"

    def handle(self, *args, **kwargs):
        commands = [
            "seed_basic",
            "seed_data",
            "seed_gaming",
            "show_data",
        ]
        for command in commands:
            try:
                print(f"Ejecutando: {command}")
                call_command(command)
            except Exception as e:
                print(f"Error al ejecutar {command}: {e}")
