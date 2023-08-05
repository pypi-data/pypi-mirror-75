# Django
from django.core.management.commands.makemigrations import (
    Command as CoreMakeMigrationsCommand
)

# Project
from ...utils import get_producer_models, validate_models


class Command(CoreMakeMigrationsCommand):
    def handle(self, *args, **options):
        models = get_producer_models()
        validate_models(models)
        return super().handle(*args, **options)
