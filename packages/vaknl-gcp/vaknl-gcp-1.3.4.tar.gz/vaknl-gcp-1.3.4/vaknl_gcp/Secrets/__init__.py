"""Extra functions for Google Cloud Secret manager"""

__author__ = "Wytze Bruinsma"

import json

from google.cloud.secretmanager_v1 import SecretManagerServiceClient


class SecretsClient(SecretManagerServiceClient):

    def __init__(self, project, **kwargs):
        self.project = project
        super().__init__(**kwargs)

    def get_default_secret(self, secret_id):
        version_id = 'latest'
        name = super().secret_version_path(self.project, secret_id, version_id)
        response = super().access_secret_version(name)
        return json.loads(response.payload.data.decode('UTF-8'))
