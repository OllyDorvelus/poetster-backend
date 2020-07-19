# from __future__ import absolute_import, unicode_literals
#
# import os
#
# from celery import Celery
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poetster.settings')
# os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
#
# import configurations
# configurations.setup()
#
# app = Celery('poetster')
#
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
#
# # sample for scheduling task
# # app.conf.beat_schedule = {
# #     'display_time-30-seconds': {
# #         'task': 'poem.tasks.display_time',
# #         'schedule': 10.0
# #     },
# # }