import os

from boto3 import client, resource
from pyqldb.driver.pooled_qldb_driver import PooledQldbDriver


class FlaskQldb(object):
    """
    This is a helper extension, which adjusts flask_qldb configuration for the
    application.
    """

    def __init__(self, app=None):
        self._app = app
        self._default_ledger_name = None
        self._aws_credentials = None
        self._client = None
        self._resource = None
        self._drivers = dict()

        if app:
            self.init_app(app)

    def init_app(self, app):
        self._app = app
        self._default_ledger_name = self._app.config.get('LEDGER_NAME')
        self.client()
        self.driver()

    def client(self, service_name='qldb'):
        if self._client:
            return self._client

        credentials = self.get_aws_credentials()
        self._client = client(service_name,
                              region_name=credentials['region_name'],
                              aws_access_key_id=credentials['aws_access_key_id'],
                              aws_secret_access_key=credentials['aws_secret_access_key'],
                              # endpoint_url='http://localhost:8000',
                              # verify=False
                              )
        return self._client

    def resource(self, resource_name='s3'):
        if self._resource:
            return self._resource

        credentials = self.get_aws_credentials()
        self._client = resource(resource_name,
                                region_name=credentials['region_name'],
                                aws_access_key_id=credentials['aws_access_key_id'],
                                aws_secret_access_key=credentials['aws_secret_access_key'],
                                )
        return self._client

    def driver(self, ledger_name=None):
        if not ledger_name:
            ledger_name = self._default_ledger_name

        if ledger_name in self._drivers:
            return self._drivers.get(ledger_name)

        credentials = self.get_aws_credentials()

        self._drivers[ledger_name] = PooledQldbDriver(
            ledger_name=ledger_name,
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],
        )
        return self._drivers[ledger_name]

    def session(self, ledger_name=None):
        if not ledger_name:
            ledger_name = self._default_ledger_name

        return self.driver(ledger_name).get_session()

    def _get_value(self, name):
        value = self._app.config.get(name)
        return value if value else os.getenv(name, None)

    def get_aws_credentials(self):
        if self._aws_credentials:
            return self._aws_credentials

        self._aws_credentials = dict(
            region_name=self._get_value('AWS_REGION'),
            aws_access_key_id=self._get_value('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=self._get_value('AWS_SECRET_ACCESS_KEY')
        )

        return self._aws_credentials
