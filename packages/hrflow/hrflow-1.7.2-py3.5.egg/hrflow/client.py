import requests as req
import json

from hrflow.job import Job
from .profile import Profile
from .webhook import Webhook
from .source import Source
from .utils import validate_params


CLIENT_API_URL = "https://api.hrflow.ai/v1/"


class Client(object):
    """client api wrapper client."""

    def __init__(self, api_url=CLIENT_API_URL, api_secret=None, webhook_secret=None):
        """Init."""
        self.api_url = api_url
        self.auth_header = {
            "X-API-Key": api_secret
        }
        self.webhook_secret = webhook_secret
        self.job = Job(self)
        self.profile = Profile(self)
        self.webhooks = Webhook(self)
        self.source = Source(self)

    def _create_request_url(self, resource_url):
        return "{api_endpoint}{resource_url}".format(
            api_endpoint=self.api_url,
            resource_url=resource_url
        )

    def _fill_headers(self, header, base={}):
        for key, value in header.items():
            base[key] = value
        return base

    def _prepare_params_for_file_upload(self, bodyparams):
        for key, value in bodyparams.items():
            if isinstance(value, dict) or isinstance(value, list):
                bodyparams[key] = json.dumps(value)
        return bodyparams

    def get(self, resource_endpoint, query_params={}):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        if query_params:
            return req.get(url, headers=self.auth_header, params=validate_params(query_params))
        else:
            return req.get(url, headers=self.auth_header)

    def post(self, resource_endpoint, data={}, json={}, files=None):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        if files:
            data = self._prepare_params_for_file_upload(data)
            return req.post(url, headers=self.auth_header, files=files, data=data)
        else:
            return req.post(url, headers=self.auth_header, data=data, json=json)

    def patch(self, resource_endpoint, data={}):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        return req.patch(url, headers=self.auth_header, data=data)

    def put(self, resource_endpoint, json={}):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        return req.put(url, headers=self.auth_header, json=json)
