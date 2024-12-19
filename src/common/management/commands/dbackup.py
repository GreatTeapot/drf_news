from datetime import datetime

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """
    Command for creating backups
    """

    def handle(self, *args, **options):
        """
        Method to run a custom command.
        """
        self.stdout.write('Waiting for database copy')
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--indent=2',
            '--exclude=contenttypes',
            '--exclude=admin.logentry',
            f'--output=database-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json',
        )
        self.stdout.write(
            self.style.SUCCESS('Database backup created successfully')
        )
