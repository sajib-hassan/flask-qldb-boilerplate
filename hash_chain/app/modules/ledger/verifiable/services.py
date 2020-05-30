from http import HTTPStatus

from hash_chain.app.extensions import logger
from hash_chain.app.extensions.flask_qldb.connect_to_ledger import create_qldb_session
from hash_chain.app.modules.ledger.core.get_block import get_digest_result, verify_block
from hash_chain.app.modules.ledger.core.get_revision import query_revision_history
from hash_chain.app.modules.ledger.helpers import get_requested_data
from hash_chain.app.util import fail_response


class VerifiableServices(object):
    def get_digest_result(self):
        """Retrieving the digest of a particular ledger."""
        try:
            data = get_requested_data()
            digest = get_digest_result(data["ledger_name"])
            return digest
        except Exception as e:
            logger.exception('Unable to get a ledger digest!')
            return fail_response('Unable to delete the ledger. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    def verify_block(self):
        """
        Get a journal block from a QLDB ledger.

        After getting the block, we get the digest of the ledger and validate the
        proof returned in the getBlock response.
        """
        try:
            data = get_requested_data()
            with create_qldb_session(data["ledger_name"]) as session:
                cursor = session.execute_lambda(lambda executor: query_revision_history(executor,
                                                                                        data["table_name"],
                                                                                        data["condition_str"],
                                                                                        data["condition_value"]),
                                                lambda retry_indicator: logger.info('Retrying due to OCC conflict...'))
                row = next(cursor)
                block_address = row.get('blockAddress')
                verify_block(data["ledger_name"], block_address)
        except Exception:
            logger.exception('Unable to query vehicle registration by Vin.')
