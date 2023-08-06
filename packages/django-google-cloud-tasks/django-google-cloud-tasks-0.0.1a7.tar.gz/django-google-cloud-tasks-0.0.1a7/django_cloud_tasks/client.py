# pylint: disable=not-callable, unsubscriptable-object
import base64
import json
import logging
import os
from datetime import datetime, timedelta

import google
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import tasks_v2
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2

from django_cloud_tasks import exceptions

logger = logging.getLogger(__name__)


class BaseGoogleCloud:
    _config = None
    _credentials = None
    _client_class = None
    _scopes = ['https://www.googleapis.com/auth/cloud-platform']
    _project_id = None

    def __init__(self, subject=None, **kwargs):
        self._credentials, self._project_id = self.get_credentials(subject=subject)
        self.client = self._client_class(
            credentials=self._credentials,
            **kwargs
        )

    @classmethod
    def get_credentials(cls, subject=None):
        try:
            if 'GCP_B64' in os.environ:
                config = json.loads(base64.b64decode(os.environ.get('GCP_B64')))
                credentials = service_account.Credentials.from_service_account_info(config)
                credentials = credentials.with_scopes(cls._scopes)
                if subject:
                    credentials = credentials.with_subject(subject=subject)
                project_id = config.get('project_id')
            else:
                credentials, project_id = google.auth.default(scopes=cls._scopes)
        except (TypeError, KeyError, DefaultCredentialsError) as e:
            raise exceptions.GoogleCredentialsException(e)

        return credentials, project_id

    @classmethod
    def encode_credential(cls, json_str):
        return base64.b64encode(json_str.encode()).decode()


class CloudTasksClient(BaseGoogleCloud):
    _client_class = tasks_v2.CloudTasksClient

    def push(self, queue, url, payload, delay_in_seconds=0, location='us-east1', task_id=None):
        parent = self.client.queue_path(project=self._project_id, location=location, queue=queue)

        task = {
            'http_request': {
                'http_method': 'POST',
                'url': url,
                'body': payload.encode(),
            },
        }

        if task_id:
            task['name'] = self.client.task_path(project=self._project_id, location=location, queue=queue, task=task_id)

        if delay_in_seconds:
            target_date = datetime.utcnow() + timedelta(seconds=delay_in_seconds)
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(target_date)

            task['schedule_time'] = timestamp

        response = self.client.create_task(parent, task)
        return response
