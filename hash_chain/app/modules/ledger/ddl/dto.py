from flask_restx import Namespace, fields

from hash_chain.app.extensions.app_config import config


class DdlDto:
    api = Namespace('ddl', description='Ledger related operations')
    ledger_create = api.model('ledger_create', {
        'ledger_name': fields.String(required=False, description='Valid ledger name on QLDB',
                                     default=f"{config.LEDGER_NAME}"),
    })

    ledgers = api.model('ledgers', {
        'name': fields.String(required=True, description='ledger name', attribute='Name'),
        'state': fields.String(required=True, description='ledger state', attribute="State"),
        'creation_datetime': fields.DateTime(required=True, description='ledger creation datetime',
                                             attribute="CreationDateTime"),
    })

    ledger = api.clone('ledger', ledgers, {
        'arn': fields.String(required=True, description='ledger Arn', attribute='Arn'),
        'deletion_protection': fields.Boolean(required=True, description='ledger deletion protection',
                                              attribute='DeletionProtection'),
    })
