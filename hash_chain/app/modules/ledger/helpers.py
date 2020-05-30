from time import sleep

from flask import request

from hash_chain.app.extensions import logger
from hash_chain.app.extensions.flask_qldb import qldb_client
from hash_chain.app.extensions.app_config import config


def get_requested_data(self):
    data = request.json
    if "ledger_name" in data and not data["ledger_name"].strip():
        data["ledger_name"] = config.LEDGER_NAME
    return data

def describe_ledger(ledger_name):
    logger.info('describe ledger with name: {}.'.format(ledger_name))
    result = qldb_client.describe_ledger(Name=ledger_name)
    result.pop('ResponseMetadata')
    logger.info('Success. Ledger description: {}.'.format(result))
    return result


def set_deletion_protection(ledger_name, deletion_protection):
    """
    Update an existing ledger's deletion protection.

    :type ledger_name: str
    :param ledger_name: Name of the ledger to update.

    :type deletion_protection: bool
    :param deletion_protection: Enable or disable the deletion protection.

    :rtype: dict
    :return: Result from the request.
    """
    logger.info("Let's set deletion protection to {} for the ledger with name {}.".format(deletion_protection,
                                                                                          ledger_name))
    result = qldb_client.update_ledger(Name=ledger_name, DeletionProtection=deletion_protection)
    logger.info('Success. Ledger updated: {}'.format(result))


def wait_for_active(ledger_name):
    while True:
        result = describe_ledger(ledger_name=ledger_name)
        if result.get('State') == config.ACTIVE_STATE:
            logger.info('Success. Ledger is active and ready to use.')
            return result

        sleep(config.LEDGER_CREATION_POLL_PERIOD_SEC)


def wait_for_deleted(self, ledger_name):
    logger.info('Waiting for the ledger to be deleted...')
    while True:
        try:
            describe_ledger(ledger_name)
            logger.info('The ledger is still being deleted. Please wait...')
            sleep(config.LEDGER_DELETION_POLL_PERIOD_SEC)
        except qldb_client.exceptions.ResourceNotFoundException:
            logger.info('Success. The ledger is deleted.')
            break
