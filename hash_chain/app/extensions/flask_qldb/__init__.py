from boto3 import client

qldb_client = client('qldb')

def init_app(app, **kwargs):
    """
    flask_qldb extension initialization point.
    """
    pass

