from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Executes model training routine and updates DB with new hyper parameters'

    def handle(self, *args, **options):
        from rdtm.tasks import train_and_update_db

        self.stdout.write(self.style.SUCCESS('Training in progress...'))
        accuracy = train_and_update_db()
        self.stdout.write(self.style.SUCCESS('Training completed!'))
        self.stdout.write(self.style.SUCCESS('Accuracy: %.2f%%' % accuracy))
