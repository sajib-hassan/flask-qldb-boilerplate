# encoding: utf-8
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""
from .logging import Logging

logger = Logging()

from .flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import api, flask_qldb, flask_bcrypt, app_config


def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
            logger,
            db,
            flask_bcrypt,
            api,
            flask_qldb,
            app_config
    ):
        extension.init_app(app)
