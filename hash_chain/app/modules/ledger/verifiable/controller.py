# encoding: utf-8
from http import HTTPStatus

from flask_restx import Resource

from hash_chain.app.modules.auth.decorators import admin_token_required
from hash_chain.app.modules.ledger.verifiable.dto import VerifiableDto
from hash_chain.app.modules.ledger.verifiable.services import VerifiableServices

api = VerifiableDto.api
_digest = VerifiableDto.digest
_digest_result = VerifiableDto.digest_result
_verify_block = VerifiableDto.verify_block



@api.route('/digest')
class DigestResult(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/verifiable/digest."""

    @api.doc('Retrieving the digest of a particular ledger.')
    @api.expect(_digest, validate=True)
    @api.doc(security="jwt_token")
    @admin_token_required
    @api.marshal_list_with(_digest_result, envelope='data')
    @api.response(int(HTTPStatus.OK), "Retrieving the digest.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the ledger.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Retrieving the digest of a particular ledger."""
        return VerifiableServices().create_ledger_action()


@api.route('/verify_block')
class VerifyBlock(Resource):
    """Handles HTTP requests to URL: /api/v1/ledger/verifiable/verify_block."""

    @api.doc('Get a journal block from a QLDB ledger.')
    @api.expect(_verify_block, validate=True)
    @api.doc(security="jwt_token")
    @admin_token_required
    # @api.marshal_list_with(_verify_block, envelope='data')
    @api.response(int(HTTPStatus.CREATED), "Ledger is active and ready to use.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Unable to create the ledger.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        """Get a journal block from a QLDB ledger."""
        return VerifiableServices().verify_block()

