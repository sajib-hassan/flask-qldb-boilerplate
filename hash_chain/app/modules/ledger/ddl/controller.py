# encoding: utf-8
from http import HTTPStatus

from flask_restx import Resource

from hash_chain.app.modules.auth.decorators import admin_token_required
from hash_chain.app.modules.ledger.ddl.dto import DdlDto
from hash_chain.app.modules.ledger.ddl.services import DdlServices

api = DdlDto.api
ledger_create = DdlDto.ledger_create
table_create = DdlDto.table_create
ledger_delete = DdlDto.ledger_delete
table_index_create = DdlDto.table_index_create


@api.route('/')
class Ledger(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/ddl/."""

    @api.doc('Create QLDB Ledger')
    @api.doc(security="jwt_token")
    @api.expect(ledger_create, validate=True)
    @admin_token_required
    @api.response(int(HTTPStatus.CREATED), "Ledger is active and ready to use.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the ledger.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Create QLDB Ledger"""
        return DdlServices().create_ledger_action()

    @api.doc('Delete QLDB Ledger')
    @api.expect(ledger_delete, validate=True)
    @api.doc(security="jwt_token")
    @admin_token_required
    @api.response(int(HTTPStatus.ACCEPTED), "The ledger is successfully deleted.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to delete the ledger.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def delete(self):
        """Delete QLDB Ledger"""
        return DdlServices().delete_ledger_action()


@api.route('/table')
class LedgerTable(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/ddl/table."""

    @api.doc('Create QLDB Table')
    @api.expect(table_create, validate=True)
    @api.doc(security="jwt_token")
    @admin_token_required
    @api.response(int(HTTPStatus.CREATED), "Tables created successfully.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the table.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Create QLDB Table"""
        return DdlServices().create_table_action()


@api.route('/table_index')
class LedgerTableIndex(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/ddl/table_index."""

    @api.doc('Create index on table in a particular ledger')
    @api.expect(table_create, validate=True)
    @api.doc(security="jwt_token")
    @admin_token_required
    @api.response(int(HTTPStatus.CREATED), "Index created successfully.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the index.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Create index on table in a particular ledger"""
        return DdlServices().create_table_index_action()
