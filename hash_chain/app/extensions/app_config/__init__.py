from flask import current_app


class Config(object):
    def __getattr__(self, name):
        if name not in current_app.config:
            raise AttributeError("'Application Config' object has no attribute '%s'" % name)
        return current_app.config.get(name)


config = Config()


def init_app(app, **kwargs):
    pass
