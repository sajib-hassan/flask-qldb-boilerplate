# encoding: utf-8
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""
from .logging import Logging

logging = Logging()

from .flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .flask_qldb import FlaskQldb

qldb = FlaskQldb()

from . import api, flask_bcrypt, app_config


def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
            flask_bcrypt,
            app_config,
            logging,
            api,
            db,
            qldb,
    ):
        extension.init_app(app)
