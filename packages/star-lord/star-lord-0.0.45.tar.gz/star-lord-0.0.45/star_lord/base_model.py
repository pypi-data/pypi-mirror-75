# Django
from django.db import models

# Project
from .delete_model import DeleteModel


class ModifyDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class BaseModel(ModifyDateModel, DeleteModel):
    class Meta:
        abstract = True
        ordering = ['-id']
