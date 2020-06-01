import time
from functools import reduce
from sys import argv

from boto3 import client, resource

from hash_chain.app.extensions import logger
from hash_chain.app.extensions.app_config import config
from hash_chain.app.modules.ledger.core.export_journal import create_s3_bucket_if_not_exists, \
    create_export_and_wait_for_completion, set_up_s3_encryption_configuration, describe_journal_export
from hash_chain.app.modules.ledger.core.verifier import join_hash_pairwise


def create_journal_export():
    """
    Export journal contents to a S3 bucket.

    :rtype: str
    :return: The ExportId fo the journal export.
    """
    s3_resource = resource('s3')
    sts = client('sts')

    current_time = int(time.time())
    identity = sts.get_caller_identity()
    bucket_name = '{}-{}'.format(config.JOURNAL_EXPORT_S3_BUCKET_NAME_PREFIX, identity['Account'])

    prefix = '{}-{}/'.format(config.LEDGER_NAME, current_time)
    create_s3_bucket_if_not_exists(bucket_name, s3_resource)

    export_journal_to_s3_result = create_export_and_wait_for_completion(config.LEDGER_NAME, bucket_name, prefix,
                                                                        set_up_s3_encryption_configuration())

    return export_journal_to_s3_result.get('ExportId')


def compare_journal_blocks(previous_journal_block, journal_block):
    """
    Compare the hash values on the given journal blocks.

    :type previous_journal_block: :py:class:`hash_chain.ledger.qldb.journal_block.JournalBlock`
    :param previous_journal_block: Previous journal block in the chain.

    :type journal_block: :py:class:`hash_chain.ledger.qldb.journal_block.JournalBlock`
    :param journal_block: Current journal block in the chain.

    :rtype: :py:class:`hash_chain.ledger.qldb.journal_block.JournalBlock`
    :return: The current journal block in the chain.

    :raises RuntimeError: If the chain hash on the journal block is broken.
    """
    if previous_journal_block is None:
        return journal_block
    if previous_journal_block.block_hash != journal_block.previous_block_hash:
        raise RuntimeError('Previous block hash does not match!')

    block_hash = join_hash_pairwise(journal_block.entries_hash, previous_journal_block.block_hash)
    if block_hash != journal_block.block_hash:
        raise RuntimeError("Block hash doesn't match expected block hash. Verification failed.")

    return journal_block


def verify(journal_blocks):
    """
    Validate that the chain hash on the journal block is valid.

    :type journal_blocks: list
    :param journal_blocks: A list of journal blocks.

    :return: None if the given list of journal blocks is empty.
    """
    if len(journal_blocks) == 0:
        return
    reduce(compare_journal_blocks, journal_blocks)


if __name__ == '__main__':
    """
    Validate the hash chain of a QLDB ledger by stepping through its S3 export.
    
    This code accepts an exportID as an argument, if exportID is passed the code 
    will use that or request QLDB to generate a new export to perform QLDB hash 
    chain validation.
    """
    s3_client = client('s3')
    try:
        if len(argv) == 2:
            export_id = argv[1]
            logger.info('Validating qldb hash chain for ExportId: {}.'.format(export_id))

        else:
            logger.info('Requesting qldb to create an export.')
            export_id = create_journal_export()

        journal_export = describe_journal_export(config.LEDGER_NAME, export_id).get('ExportDescription')
        journal_blocks = read_export(journal_export, s3_client)
        verify(journal_blocks)
    except Exception:
        logger.exception('Unable to perform hash chain verification.')
