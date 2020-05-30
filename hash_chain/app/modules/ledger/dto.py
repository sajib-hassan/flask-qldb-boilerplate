from flask_restx import Namespace


class LedgerDto:
    api = Namespace('ledger', description='Ledger related operations')
