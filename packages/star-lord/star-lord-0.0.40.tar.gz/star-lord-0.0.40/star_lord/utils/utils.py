# Django
from django.db.models import ManyToManyField, OneToOneField, ForeignKey
from django.db import connection
from django.apps import apps

# Project
from ..amqp.job import JobClient


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_new_fields(model):
    table_name = model._meta.db_table
    current_fields = [i.name for i in model._meta.fields]

    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name "
                       "FROM INFORMATION_SCHEMA.COLUMNS "
                       "WHERE TABLE_NAME = %s", [table_name])
        db_fields = [i['column_name'] for i in dictfetchall(cursor)]

    return set(current_fields) - set(db_fields)


def pick(keys, dict_data):
    return {key: dict_data[key] for key in keys if dict_data.get(key)}


def get_producer_models():
    models = apps.get_models()
    models = [model for model in models if hasattr(model, 'service_name')]
    return models


def get_changed_models(models):
    models = [
        model for model in models
        if get_new_fields(model) and 'id' not in get_new_fields(model)
    ]
    return models


def refresh_models(models):
    [JobClient().call(model.service_name) for model in models]


def sync_relations_data(model, data):
    relations_fields = []
    for field in model._meta.get_fields():
        is_relation = field.__class__ in [
            ManyToManyField,
            OneToOneField,
            ForeignKey
        ]
        is_consumer = hasattr(field.related_model, 'service_name')
        if is_relation and is_consumer:
            relations_fields.append(field)

    fields_sync = {i.related_model.__name__: False for i in relations_fields}

    for item in data:
        for field in relations_fields:
            name = field.get_attname()
            field_model = field.related_model
            pks = item.get(name)

            if fields_sync[field_model.__name__] or not pks:
                continue

            if field.__class__ is not ManyToManyField:
                pks = [pks]

            queryset = field_model.objects.filter(id__in=pks)
            queryset = list(queryset.values_list('id', flat=True))

            if len(queryset) != len(pks):
                JobClient().call(getattr(field_model, 'service_name'))
                fields_sync[field_model.__name__] = True


def model_sync(data, model):
    fields = [field.get_attname() for field in model._meta.fields]
    m2m_fields = [
        field.get_attname() for field in model._meta.get_fields()
        if field.__class__ is ManyToManyField
    ]
    sync_relations_data(model, data)

    for item in data:
        defaults = pick(fields, item)
        is_deleted = item.get('is_deleted')

        if is_deleted:
            model.objects.filter(id=item['id']).delete()
            continue

        model.objects.update_or_create(id=item['id'], defaults=defaults)
        if m2m_fields:
            instance = model.objects.get(id=item['id'])

            for field in m2m_fields:
                if item.get(field):
                    getattr(instance, field).set(item[field])


def validate_models(models):
    for model in models:
        msg = "%s fields type of ManyToManyField, OneToOneField, ForeignKey " \
              "must be db_constraint=False." % model.__name__

        m2m_fields = [
            field for field in model._meta.get_fields()
            if field.__class__ is ManyToManyField and
               hasattr(field.related_model, 'service_name')
        ]
        relations_fields = [
            field for field in model._meta.get_fields()
            if field.__class__ in [OneToOneField, ForeignKey] and
               hasattr(field.related_model, 'service_name')
        ]

        if m2m_fields:
            assert all(
                getattr(field.remote_field, 'db_constraint', None) is False
                for field in m2m_fields
            ), msg

        if relations_fields:
            assert all(
                getattr(field, 'db_constraint', None) is False
                for field in relations_fields
            ), msg
