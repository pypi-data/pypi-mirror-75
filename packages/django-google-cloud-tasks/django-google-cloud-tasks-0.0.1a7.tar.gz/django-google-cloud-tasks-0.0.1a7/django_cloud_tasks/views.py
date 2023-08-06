import inspect
import json

from django.apps import apps
from django.http import HttpResponse, Http404
from django.views.generic import View

from django_cloud_tasks import exceptions


class GoogleCloudTaskView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tasks = apps.get_app_config('django_cloud_tasks').tasks

    def _get_task(self, task_name):
        try:
            return self.tasks[task_name]
        except KeyError:
            raise exceptions.TaskNotFound(task_name=task_name)

    def post(self, request, task_name, *args, **kwargs):
        try:
            task_class = self._get_task(task_name=task_name)
        except exceptions.TaskNotFound as e:
            return e.response

        data = json.loads(request.body)
        output, success = task_class().execute(data=data)
        if success:
            status = 200
            result = {'result': output}
        else:
            status = 400
            result = {'error': output}

        response = HttpResponse(status=status, content=json.dumps(result), content_type='application/json')
        return response

    def get(self, request, task_name, *args, **kwargs):
        try:
            task_class = self._get_task(task_name=task_name)
        except exceptions.TaskNotFound as e:
            return e.response

        signature = inspect.signature(task_class.run)

        result = {
            'name': task_class.name(),
            'url': task_class.url(),
            'queue': task_class.queue(),
            'signature': str(signature),
        }
        response = HttpResponse(status=200, content=json.dumps(result), content_type='application/json')
        return response
