# encoding: utf-8
from http import HTTPStatus

from flask_restx import Resource

from hash_chain.app.modules.auth.decorators import admin_token_required
from hash_chain.app.modules.ledger.ddl.dto import DdlDto
from hash_chain.app.modules.ledger.ddl.services import DdlServices
from hash_chain.app.modules.ledger.parameters import ledger_name_parser_plain, table_name_parser_plain, \
    ledger_name_parser_choices_or_plain, table_index_parser_plain

api = DdlDto.api
ledgers = DdlDto.ledgers
ledger = DdlDto.ledger

ledger_name_plain = ledger_name_parser_plain(default=None)
ledger_name_choices = ledger_name_parser_choices_or_plain(location='args')
table_name = table_name_parser_plain()
table_index_create = table_index_parser_plain()


@api.route('/ledgers')
@api.doc(security="jwt_token")
@api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
@api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Ledger(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/ddl/."""

    @api.doc('List all QLDB ledgers in a given account')
    @admin_token_required
    @api.marshal_list_with(ledgers, envelope='data')
    @api.response(int(HTTPStatus.OK), "Found all ledger.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the ledger.")
    def get(self):
        """List all QLDB ledgers in a given account"""
        return DdlServices.get_ledger_list()

    @api.doc('Returns information about a ledger, including its state and when it was created')
    @admin_token_required
    @api.expect(ledger_name_choices, validate=True)
    @api.marshal_with(ledger, envelope='data')
    @api.response(int(HTTPStatus.NOT_FOUND), "Ledger Not Found.")
    @api.response(int(HTTPStatus.OK), "Retrieving the digest.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to connect ledgers.")
    def get(self):
        """Returns information about a ledger, including its state and when it was created."""
        args = ledger_name_choices.parse_args(req=None, strict=False)
        return DdlServices.describe_ledger(**args)

    @api.doc('Create QLDB Ledger')
    @admin_token_required
    @api.expect(ledger_name_plain, validate=True)
    @api.response(int(HTTPStatus.CREATED), "Ledger is active and ready to use.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the ledger.")
    def post(self):
        """Create QLDB Ledger"""
        args = ledger_name_plain.parse_args(req=None, strict=False)
        return DdlServices.create_ledger(**args)

    @api.doc('Delete QLDB Ledger')
    @admin_token_required
    @api.expect(ledger_name_choices, validate=True)
    @api.response(int(HTTPStatus.ACCEPTED), "The ledger is successfully deleted.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to delete the ledger.")
    def delete(self):
        """Delete QLDB Ledger"""
        args = ledger_name_choices.parse_args(req=None, strict=False)
        return DdlServices.delete_ledger(**args)


@api.route('/tables')
@api.doc(security="jwt_token")
@api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
@api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class LedgerTable(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/ddl/tables."""

    @api.doc('List all the tables in the configured ledger in QLDB')
    @admin_token_required
    @api.expect(ledger_name_choices, validate=True)
    @api.response(int(HTTPStatus.OK), "List of all tables.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to connect ledgers.")
    def get(self):
        """List all the tables in the configured ledger in QLDB"""
        args = ledger_name_choices.parse_args(req=None, strict=False)
        return DdlServices.list_tables(**args)

    @api.doc('Create QLDB Table')
    @api.expect(table_name, validate=True)
    @api.response(int(HTTPStatus.CREATED), "Tables created successfully.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the table.")
    @admin_token_required
    def post(self):
        """Create QLDB Table"""
        args = table_name.parse_args(req=None, strict=False)
        return DdlServices.create_table(**args)

    @api.doc('Drop QLDB Table')
    @api.expect(table_name, validate=True)
    @api.response(int(HTTPStatus.ACCEPTED), "Tables dropped successfully.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to drop the table.")
    @admin_token_required
    def delete(self):
        """Drop QLDB Table"""
        args = table_name.parse_args(req=None, strict=False)
        return DdlServices.drop_table(**args)


@api.route('/table_index')
@api.doc(security="jwt_token")
@api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
@api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class LedgerTableIndex(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/ddl/table_index."""

    @api.doc('Create index on table in a particular ledger')
    @api.expect(table_index_create, validate=True)
    @admin_token_required
    @api.response(int(HTTPStatus.CREATED), "Index created successfully.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the index.")
    def post(self):
        """Create index on table in a particular ledger"""
        return DdlServices.create_table_index()
