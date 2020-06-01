import os
import sys

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'staging': 'config.StagingConfig',
    'production': 'config.ProductionConfig',
    'local': 'local_config.LocalConfig',
}


def create_app(flask_config_name=None, **kwargs):
    """
    Entry point to the Flask RESTx Server application.
    """
    import threading
    threading.stack_size(2 * 1024 * 1024)

    app = Flask(__name__, **kwargs)

    env_flask_config_name = os.getenv('FLASK_ENV')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'local'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                    "FLASK_ENV environment variable (\"%s\") and flask_config_name argument "
                    "(\"%s\") are both set and are not the same." % (
                        env_flask_config_name,
                        flask_config_name
                    )
            )

    try:
        app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])
    except ImportError:
        if flask_config_name == 'local':
            app.logger.error(
                "You have to have `local_config.py` or `local_config/__init__.py` in order to use "
                "the default 'local' Flask Config. Alternatively, you may set `FLASK_CONFIG` "
                "environment variable to one of the following options: `development`, `production`, "
                "`staging`, `testing` after copied `config.py.sample` to `config.py`"
            )
            sys.exit(1)
        raise

    # ensure the instance folder exists
    try:
        os.makedirs(app.config.get('PROJECT_INSTANCE_DIR'))
    except OSError:
        pass

    if app.config['REVERSE_PROXY_SETUP']:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    with app.app_context():
        from . import extensions
        extensions.init_app(app)

        from . import modules
        modules.init_app(app)

    return app
