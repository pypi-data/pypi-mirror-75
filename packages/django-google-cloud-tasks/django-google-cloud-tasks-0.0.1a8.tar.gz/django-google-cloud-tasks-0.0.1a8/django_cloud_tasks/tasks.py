import json
from abc import ABC, abstractmethod

from django.apps import apps
from django.urls import reverse

from django_cloud_tasks.client import CloudTasksClient


class BaseTask(ABC):
    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError()

    def execute(self, data):
        try:
            output = self.run(**data)
            success = True
        except Exception as e:  # pylint: disable=broad-except
            output = str(e)
            success = False
        return output, success

    def delay(self, params=None, **kwargs):
        payload = params or {}

        return self.__client.push(
            queue=self.queue(),
            url=self.url(),
            payload=json.dumps(payload),
            **kwargs
        )

    def retry(self, data):
        return self.delay(params=data)

    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def queue(cls):
        return 'tasks'

    @classmethod
    def url(cls):
        domain = apps.get_app_config('django_cloud_tasks').domain
        path = reverse('tasks-endpoint', args=(cls.name(),))
        return f'{domain}{path}'

    @property
    def __client(self):
        return CloudTasksClient()
