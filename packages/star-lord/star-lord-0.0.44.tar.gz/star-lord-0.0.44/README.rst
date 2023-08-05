Installing star-lord
------------------------

The package can be installed using:

.. code-block:: bash

    pip install star-lord

Add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'star_lord',
    )


Creating models
---------------

Mark model as producer using "producer" decorator:

.. code-block:: python

    from django.db import models
    from star_lord import producer


    @producer
    class MyModel(models.Model):
        ...

        @classmethod
        def get_name(cls):
            return 'my_model'

        @property
        def serialized_data(self):
            """
            Optional method which can be overridden
            """
            pass

        @staticmethod
        def signal_post_save(*args, **kwargs):
            """
            Optional method which can be overridden
            """
            pass


Creating tasks
---------------
Create file tasks.py in your app:
    my_app:
        tasks.py

.. code-block:: python

    from star_lord import model_sync, job_tasks
    from .models import User, Employee

    job_tasks('auth.usr.changed', model=User)(model_sync)
    job_tasks('hrm.emp.changed')(Employee.sync)


