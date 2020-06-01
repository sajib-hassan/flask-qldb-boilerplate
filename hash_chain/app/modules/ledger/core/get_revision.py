from hash_chain.app.extensions import logger
from hash_chain.app.extensions.flask_qldb import qldb_client
from hash_chain.app.modules.ledger.core.utils import convert_object_to_ion


def get_revision(ledger_name, document_id, block_address, digest_tip_address):
    """
    Get the revision data object for a specified document ID and block address.
    Also returns a proof of the specified revision for verification.

    :type ledger_name: str
    :param ledger_name: Name of the ledger containing the document to query.

    :type document_id: str
    :param document_id: Unique ID for the document to be verified, contained in the committed view of the document.

    :type block_address: dict
    :param block_address: The location of the block to request.

    :type digest_tip_address: dict
    :param digest_tip_address: The latest block location covered by the digest.

    :rtype: dict
    :return: The response of the request.
    """
    result = qldb_client.get_revision(Name=ledger_name, BlockAddress=block_address, DocumentId=document_id,
                                      DigestTipAddress=digest_tip_address)
    return result


def query_revision_history(qldb_session, table_name, condition_str, condition_value):
    """
    Query revision history for a particular vehicle for verification.

    :type qldb_session: :py:class:`pyqldb.session.qldb_session.QldbSession`
    :param qldb_session: An instance of the QldbSession class.

    :type vin: str
    :param vin: VIN to query the revision history of a specific registration with.

    :rtype: :py:class:`pyqldb.cursor.buffered_cursor.BufferedCursor`
    :return: Cursor on the result set of the statement query.
    """
    logger.info("Querying the '{}' table for the condition: {}...".format(table_name, condition_str))
    query = 'SELECT * FROM _ql_committed_{} WHERE {}'.format(table_name, condition_str)
    parameters = convert_object_to_ion(condition_value)
    cursor = qldb_session.execute_statement(query, parameters)
    return cursor
