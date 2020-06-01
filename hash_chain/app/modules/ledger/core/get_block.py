from hash_chain.app.extensions import logger
from hash_chain.app.extensions.app_config import config
from hash_chain.app.extensions.flask_qldb import qldb_client
from hash_chain.app.modules.ledger.core.block_address import block_address_to_dictionary
from hash_chain.app.modules.ledger.core.qldb_string_utils import block_response_to_string, value_holder_to_string, \
    digest_response_to_string
from hash_chain.app.modules.ledger.core.verifier import verify_document, flip_random_bit, to_base_64, parse_block


def get_digest_result(ledger_name=config.LEDGER_NAME):
    """
    Get the digest of a ledger's journal.

    :type name: str
    :param name: Name of the ledger to operate on.

    :rtype: dict
    :return: The digest in a 256-bit hash value and a block address.
    """
    logger.info("Let's get the current digest of the ledger named {}".format(ledger_name))
    result = qldb_client.get_digest(Name=ledger_name)
    logger.info('Success. LedgerDigest: {}.'.format(digest_response_to_string(result)))
    return result


def get_block(ledger_name, block_address):
    """
    Get the block of a ledger's journal.

    :type ledger_name: str
    :param ledger_name: Name of the ledger to operate on.

    :type block_address: dict
    :param block_address: The location of the block to request.

    :rtype: dict
    :return: The response of the request.
    """
    logger.info("Let's get the block for block address {} of the ledger named {}.".format(block_address, ledger_name))
    result = qldb_client.get_block(Name=ledger_name, BlockAddress=block_address)
    logger.info('Success. GetBlock: {}'.format(block_response_to_string(result)))
    return result


def get_block_with_proof(ledger_name, block_address, digest_tip_address):
    """
    Get the block of a ledger's journal. Also returns a proof of the block for verification.

    :type ledger_name: str
    :param ledger_name: Name of the ledger to operate on.

    :type block_address: dict
    :param block_address: The location of the block to request.

    :type digest_tip_address: dict
    :param digest_tip_address: The location of the digest tip.

    :rtype: dict
    :return: The response of the request.
    """
    logger.info("Let's get the block for block address {}, digest tip address {}, for the ledger named {}.".format(
        block_address, digest_tip_address, ledger_name))
    result = qldb_client.get_block(Name=ledger_name, BlockAddress=block_address,
                                   DigestTipAddress=digest_tip_address)
    logger.info('Success. GetBlock: {}.'.format(block_response_to_string(result)))
    return result


def verify_block(ledger_name, block_address):
    """
    Verify block by validating the proof returned in the getBlock response.

    :type ledger_name: str
    :param ledger_name: The ledger to get digest from.

    :type block_address: str/:py:class:`amazon.ion.simple_types.IonPyDict`
    :param block_address: The address of the block to verify.

    :raises AssertionError: When verification failed.
    """
    logger.info("Let's verify blocks for ledger with name={}.".format(ledger_name))

    try:
        logger.info("First, let's get a digest.")
        digest_result = get_digest_result(ledger_name)

        digest_tip_address = digest_result.get('DigestTipAddress')
        digest_bytes = digest_result.get('Digest')

        logger.info('Got a ledger digest. Digest end address={}, digest={}'.format(
            value_holder_to_string(digest_tip_address.get('IonText')), to_base_64(digest_bytes)))
        get_block_result = get_block_with_proof(ledger_name, block_address_to_dictionary(block_address),
                                                digest_tip_address)
        block = get_block_result.get('Block')
        block_hash = parse_block(block)

        verified = verify_document(block_hash, digest_bytes, get_block_result.get('Proof'))

        if not verified:
            raise AssertionError('Block is not verified!')
        else:
            logger.info('Success! The block is verified.')

        altered_digest = flip_random_bit(digest_bytes)
        logger.info("Let's try flipping one bit in the digest and assert that the block is NOT verified. "
                    "The altered digest is: {}".format(to_base_64(altered_digest)))

        verified = verify_document(block_hash, altered_digest, get_block_result.get('Proof'))

        if verified:
            raise AssertionError('Expected block to not be verified against altered digest.')
        else:
            logger.info('Success! As expected flipping a bit in the digest causes verification to fail.')

        altered_block_hash = flip_random_bit(block_hash)
        logger.info("Let's try flipping one bit in the block's hash and assert that the block is NOT verified. "
                    "The altered block hash is: {}.".format(to_base_64(altered_block_hash)))

        verified = verify_document(altered_block_hash, digest_bytes, get_block_result.get('Proof'))

        if verified:
            raise AssertionError('Expected altered block hash to not be verified against digest.')
        else:
            logger.info('Success! As expected flipping a bit in the block hash causes verification to fail.')
    except Exception as e:
        logger.exception('Failed to verify blocks in the ledger with name={}.'.format(ledger_name))
        raise e
