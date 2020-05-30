# encoding: utf-8
"""
Auth module
===========
"""
from hash_chain.app.extensions.api import api_v1


def init_app(app, **kwargs):
    # Touch underlying modules
    from . import controller

    # Mount authentication routes
    api_v1.add_namespace(controller.api)
