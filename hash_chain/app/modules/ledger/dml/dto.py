from flask_restx import Namespace


class DmlDto:
    api = Namespace('dml', description='QLDB Ledger DML related operations')
