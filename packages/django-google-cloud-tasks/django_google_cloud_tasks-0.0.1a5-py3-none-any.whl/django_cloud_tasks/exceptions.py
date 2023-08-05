import json

from django.http import HttpResponse


class GoogleCredentialsException(Exception):
    def __init__(self):
        message = 'GCP_B64 or GOOGLE_APPLICATION_CREDENTIALS env variable not set properly'
        super().__init__(message)


class TaskNotFound(Exception):
    def __init__(self, task_name):
        self.error = {'error': f"Task {task_name} not found"}

    @property
    def response(self):
        return HttpResponse(status=404, content=json.dumps(self.error), content_type='application/json')
