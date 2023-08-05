# Django
from django.db.models.signals import post_save, post_delete
from django.db.models import ManyToManyField
from django.conf import settings

# Project
from ..amqp.job import JobClient, job_tasks


def signal_post_save(sender, instance, created, **kwargs):
    instance.send([instance])


def signal_delete_save(sender, instance, using, **kwargs):
    if hasattr(instance, 'is_deleted'):
        instance.send([instance])
    else:
        data = [{'id': instance.id, 'is_deleted': True}]
        JobClient().call(instance.routing_key, data)


def send(routing_key):
    @staticmethod
    def wrapper(instances):
        response = []
        for i in instances:
            fields = i._meta.fields
            m2m_fields = [
                field.get_attname() for field in i._meta.get_fields()
                if field.__class__ is ManyToManyField
            ]
            data = {}
            for field in fields:
                name = field.get_attname()
                data[name] = getattr(i, name)

            for field in m2m_fields:
                data[field] = list(
                    getattr(i, field).values_list('id', flat=True)
                )

            response.append(data)
        JobClient().call(routing_key, response)

    return wrapper


def sync_model(_, model):
    if hasattr(model, 'raw_objects'):
        model.send(model.raw_objects.all())
    else:
        model.send(model.objects.all())


def producer(model):
    app_name = '%s.%s' % (settings.APP_NAME, model.get_name())
    routing_key = "%s.changed" % app_name

    model.routing_key = routing_key
    model.send = send(model.routing_key)

    job_tasks(app_name, model=model)(sync_model)

    model.signal_delete_save = signal_delete_save
    post_delete.connect(model.signal_delete_save, sender=model)

    if hasattr(model, 'post_save_trigger'):
        return model

    if not hasattr(model, 'signal_post_save'):
        model.signal_post_save = signal_post_save

    post_save.connect(model.signal_post_save, sender=model)
    return model
