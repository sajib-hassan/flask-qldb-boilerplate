from flask_restx import Namespace, fields

from hash_chain.app.extensions.app_config import config


class DdlDto:
    api = Namespace('ddl', description='Ledger related operations')
    ledger_create = api.model('ledger_create', {
        'ledger_name': fields.String(required=False, description='Valid ledger name on QLDB', default=f"{config.LEDGER_NAME}"),
    })

    table_create = api.clone('table_create', ledger_create, {
        'table_name': fields.String(required=True, description='Valid ledger table name'),
    })

    table_index_create = api.clone('table_index_create', table_create, {
        'index_attribute': fields.String(required=True, description='Valid ledger table\'s index attribute'),
    })

    ledger_delete = api.clone('ledger_delete', ledger_create, {})
