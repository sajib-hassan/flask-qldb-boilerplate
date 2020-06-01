from http import HTTPStatus

from hash_chain.app.extensions import logger
from hash_chain.app.extensions.flask_qldb import qldb_client
from hash_chain.app.extensions.flask_qldb.connect_to_ledger import create_qldb_session
from hash_chain.app.modules.ledger.helpers import wait_for_active, set_deletion_protection, wait_for_deleted, \
    get_requested_data
from hash_chain.app.util import success_response, fail_response


class DdlServices(object):
    def create_ledger_action(self):
        """Create a ledger and wait for it to be active."""
        try:
            data = get_requested_data()
            self._create_ledger(data["ledger_name"])
            wait_for_active(data["ledger_name"])
            return success_response('Ledger is active and ready to use.', HTTPStatus.CREATED)
        except Exception as e:
            logger.exception('Unable to create the ledger!')
            return fail_response('Unable to create the ledger. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    def create_table_action(self):
        """Create a Table"""
        try:
            data = get_requested_data()
            with create_qldb_session(data["ledger_name"]) as session:
                session.execute_lambda(lambda x: self._create_table(x, data["table_name"]),
                                       lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                logger.info('Table created successfully.')
                return success_response('Table created successfully.', HTTPStatus.CREATED)
        except Exception:
            logger.exception('Error creating table.')
            return fail_response('Unable to create the table. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    def create_table_index_action(self):
        """Create index on tables in a particular ledger."""
        logger.info('Creating index on all tables in a single transaction...')
        try:
            data = get_requested_data()
            with create_qldb_session(data["ledger_name"]) as session:
                session.execute_lambda(
                    lambda x: self._create_table_index(x, data["table_name"], data["index_attribute"]),
                    lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                logger.info('Index created successfully.')
                return success_response('Index created successfully.', HTTPStatus.CREATED)
        except Exception:
            logger.exception('Unable to create index.')
            return fail_response('Unable to create the index. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    def delete_ledger_action(self):
        """Delete a ledger."""
        try:
            data = get_requested_data()
            set_deletion_protection(data["ledger_name"], False)
            self._delete_ledger(data["ledger_name"])
            wait_for_deleted(data["ledger_name"])
            return success_response('The ledger is successfully deleted.', HTTPStatus.ACCEPTED)
        except Exception as e:
            logger.exception('Unable to delete the ledger.')
            return fail_response('Unable to delete the ledger. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    # protected methods
    def _create_ledger(self, name):
        logger.info("Let's create the ledger named: {}...".format(name))
        result = qldb_client.create_ledger(Name=name, PermissionsMode='ALLOW_ALL')
        logger.info('Success. Ledger state: {}.'.format(result.get('State')))
        return result

    def _create_table(self, transaction_executor, table_name):
        logger.info("Creating the '{}' table...".format(table_name))
        statement = 'CREATE TABLE {}'.format(table_name)
        cursor = transaction_executor.execute_statement(statement)
        logger.info('{} table created successfully.'.format(table_name))
        return len(list(cursor))

    def _create_table_index(self, transaction_executor, table_name, index_attribute):
        logger.info("Creating index on '{}'...".format(index_attribute))
        statement = 'CREATE INDEX on {} ({})'.format(table_name, index_attribute)
        cursor = transaction_executor.execute_statement(statement)
        return len(list(cursor))

    def _delete_ledger(self, ledger_name):
        logger.info('Attempting to delete the ledger with name: {}...'.format(ledger_name))
        result = qldb_client.delete_ledger(Name=ledger_name)
        logger.info('Success.')
        return result
