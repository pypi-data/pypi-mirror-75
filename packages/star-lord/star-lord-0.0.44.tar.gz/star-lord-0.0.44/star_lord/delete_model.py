from django.db import models
from django.db.models import QuerySet


class DeleteQuerySet(models.QuerySet):
    def delete(self):
        for item in self:
            related_fields = [
                i for i in item._meta.get_fields()
                if i.is_relation and hasattr(i, 'parent_link')
            ]

            for field in related_fields:
                name = field.get_accessor_name()
                getattr(item, name).all().delete()

            item.is_deleted = True
            item.save()


class DeleteManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return DeleteQuerySet(self.model).filter(is_deleted=False)


class DeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = DeleteManager()
    raw_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-id']

    def delete(self, using=None, keep_parents=False):
        related_fields = [
            i for i in self._meta.get_fields()
            if i.is_relation and hasattr(i, 'parent_link')
        ]

        for field in related_fields:
            name = field.get_accessor_name()
            getattr(self, name).all().delete()

        self.is_deleted = True
        self.save()
