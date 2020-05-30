from flask_restx import Namespace, fields

from hash_chain.app.extensions.app_config import config


class VerifiableDto:
    api = Namespace('verifiable', description='Ledger data verification related operations')
    digest = api.model('digest', {
        'ledger_name': fields.String(required=False, description='Valid ledger name on QLDB', default=config.LEDGER_NAME),
    })

    digest_result = api.model('digest_result', {
        'digest': fields.String(required=True, description='digest hash'),
        'digestTipAddress': fields.String(required=True, description='digest tip address'),
        'ledger': fields.String(required=True, description='ledger name'),
        'date': fields.String(required=True, description='date of digest results'),
    })

    verify_block = api.clone('verify_block', digest_result, {
        'table_name': fields.String(required=True, description='table name'),
        'condition_str': fields.String(required=True, description='condition string "Condition = ?"'),
        'condition_value': fields.String(required=True, description='condition value'),
    })



