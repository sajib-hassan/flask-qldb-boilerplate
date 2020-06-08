# encoding: utf-8
from http import HTTPStatus

from flask_restx import Resource

from hash_chain.app.modules.auth.decorators import admin_token_required
from hash_chain.app.modules.ledger.dml.dto import DmlDto
from hash_chain.app.modules.ledger.dml.services import DmlServices
from hash_chain.app.modules.ledger.parameters import table_name_parser_plain

api = DmlDto.api

table_name = table_name_parser_plain()


@api.route('/documents')
@api.doc(security="jwt_token")
@api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
@api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class LedgerTableDocument(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/dml/documents."""

    @api.doc('Insert documents into a table in a QLDB ledger.')
    @api.expect(table_name, validate=True)
    @admin_token_required
    @api.response(int(HTTPStatus.CREATED), "Documents inserted successfully.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to insert documents.")
    def post(self):
        """Insert documents into a table in a QLDB ledger."""
        args = table_name.parse_args(req=None, strict=False)
        return DmlServices.do_insert_documents(**args)

    @api.doc('Get documents from a table in a QLDB ledger.')
    @api.expect(table_name, validate=True)
    @admin_token_required
    @api.response(int(HTTPStatus.CREATED), "Documents retrieved successfully.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to retrieve documents.")
    def get(self):
        """Retrieve documents from a table in a QLDB ledger."""
        pass
