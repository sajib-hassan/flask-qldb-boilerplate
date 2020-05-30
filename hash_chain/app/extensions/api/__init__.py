# encoding: utf-8
"""
API extension
=============
"""

from copy import deepcopy

from .api import Api

api_v1 = Api(
    title='HashChain APIs',
    version='0.1.0',
    doc='/doc',
    description='It is a [real-life example Web services for <strong>HashChain</strong> implementation '
                'using Flask-RESTx] <style>.swagger-ui section.models.is-open {display: none !important}</style>',
)


def init_app(app, **kwargs):
    """
    API extension initialization point.
    """
    # Prevent config variable modification with runtime changes
    api_v1.authorizations = deepcopy(app.config['AUTHORIZATIONS'])
