# Django
from django.core.management.commands.migrate import (
    Command as CoreMigrateCommand
)

# Project
from ...utils import get_changed_models, refresh_models, get_producer_models


class Command(CoreMigrateCommand):
    def handle(self, *args, **options):
        models = get_producer_models()
        models = get_changed_models(models)

        super().handle(*args, **options)
        refresh_models(models)
