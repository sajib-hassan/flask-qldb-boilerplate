# encoding: utf-8
"""
QLDB Ledger module
============
"""

from hash_chain.app.extensions.api import api_v1
from hash_chain.app.modules.ledger.dto import LedgerDto


def init_app(app, **kwargs):
    # Touch underlying modules
    api_v1.add_namespace(LedgerDto.api)

    from importlib import import_module

    for module_name in app.config['ENABLED_LEDGER_MODULES']:
        import_module('.%s' % module_name, package=__name__).init_app(app, **kwargs)
