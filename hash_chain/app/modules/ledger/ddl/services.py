from http import HTTPStatus

from hash_chain.app.extensions import qldb
from hash_chain.app.extensions.logging import logger
from hash_chain.app.modules.ledger.helpers import wait_for_active, set_deletion_protection, wait_for_deleted
from hash_chain.app.util import success_response, fail_response


class DdlServices(object):
    ledgers = None

    @staticmethod
    def create_ledger(ledger_name):
        """Create a ledger and wait for it to be active."""
        try:
            DdlServices.do_create_ledger(ledger_name)
            wait_for_active(ledger_name)
            DdlServices.reset_ledgers()
            return success_response('Ledger is active and ready to use.', HTTPStatus.CREATED)
        except Exception as e:
            logger.exception('Unable to create the ledger!')
            return fail_response('Unable to create the ledger. error: {}. Please try again.'.format(e),
                                 HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def create_table(ledger_name=None, table_name=None):
        """Create a Table"""
        try:
            with qldb.session(ledger_name) as session:
                session.execute_lambda(lambda x: DdlServices.do_create_table(x, table_name),
                                       lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                logger.info('Table created successfully.')
                return success_response('Table created successfully.', HTTPStatus.CREATED)
        except Exception:
            logger.exception('Error creating table.')
            return fail_response('Unable to create the table. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def drop_table(ledger_name=None, table_name=None):
        """Create a Table"""
        try:
            with qldb.session(ledger_name) as session:
                session.execute_lambda(lambda x: DdlServices.do_drop_table(x, table_name),
                                       lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                logger.info('Table dropped successfully.')
                return success_response('Table dropped successfully.', HTTPStatus.CREATED)
        except Exception:
            logger.exception('Error creating table.')
            return fail_response('Unable to create the table. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def create_table_index(ledger_name=None, table_name=None, index_attribute=None):
        """Create index on tables in a particular ledger."""
        logger.info('Creating index on all tables in a single transaction...')
        try:
            with qldb.session(ledger_name) as session:
                session.execute_lambda(
                    lambda x: DdlServices.do_create_table_index(x, table_name, index_attribute),
                    lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                logger.info('Index created successfully.')
                return success_response('Index created successfully.', HTTPStatus.CREATED)
        except Exception:
            logger.exception('Unable to create index.')
            return fail_response('Unable to create the index. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def delete_ledger(ledger_name):
        """Delete a ledger."""
        try:
            set_deletion_protection(ledger_name, False)
            DdlServices.do_delete_ledger(ledger_name)
            wait_for_deleted(ledger_name)
            DdlServices.reset_ledgers()
            return success_response('The ledger is successfully deleted.', HTTPStatus.ACCEPTED)
        except Exception as e:
            logger.exception('Unable to delete the ledger.')
            return fail_response('Unable to delete the ledger. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def reset_ledgers():
        DdlServices.ledgers = None

    @staticmethod
    def list_tables(ledger_name):
        """
            Connect to a session for a given ledger using default settings.
            """
        try:
            qldb_session = qldb.session(ledger_name)
            logger.info('Listing table names ')
            tables = qldb_session.list_tables()
            _tables = []
            for table in tables:
                _tables.append(table)
            return _tables
        except Exception as e:
            logger.exception('Unable to create session.')
            return fail_response('Unable to connect ledgers!. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def get_ledger_list():
        """
        List all ledgers.

        :rtype: list
        :return: List of ledgers.
        """
        try:
            logger.info("Let's list all the ledgers...")
            ledgers = DdlServices.ledger_list()
            logger.info('Success. List of ledgers: {}.'.format(ledgers))
            return ledgers
        except Exception as e:
            logger.exception('Unable to list ledgers!')
            return fail_response('Unable to list ledgers!. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def describe_ledger(ledger_name):
        """
        Returns information about a ledger, including its state and when it was created.
        """
        try:
            logger.info("Let's describe ledger...{}".format(ledger_name))
            ledger = qldb.client().describe_ledger(Name=ledger_name)
            logger.info('Success. describe ledger...{}.'.format(ledger))
            return ledger
        except Exception as e:
            logger.exception('Unable to list ledgers!')
            return fail_response('Unable to list ledgers!. Please try again.', HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def ledger_list():
        if DdlServices.ledgers:
            logger.info('Loaded from cash: {}.'.format(DdlServices.ledgers))
            return DdlServices.ledgers

        result = qldb.client().list_ledgers()
        DdlServices.ledgers = result.get('Ledgers')
        return DdlServices.ledgers

    # protected methods

    @staticmethod
    def do_create_ledger(name):
        logger.info("Let's create the ledger named: {}...".format(name))
        result = qldb.client().create_ledger(Name=name, PermissionsMode='ALLOW_ALL')
        logger.info('Success. Ledger state: {}.'.format(result.get('State')))
        return result

    @staticmethod
    def do_create_table(transaction_executor, table_name):
        logger.info("Creating the '{}' table...".format(table_name))
        statement = 'CREATE TABLE {}'.format(table_name)
        cursor = transaction_executor.execute_statement(statement)
        logger.info('{} table created successfully.'.format(table_name))
        return len(list(cursor))

    @staticmethod
    def do_drop_table(transaction_executor, table_name):
        logger.info("Drop the '{}' table...".format(table_name))
        statement = 'DROP TABLE {}'.format(table_name)
        cursor = transaction_executor.execute_statement(statement)
        logger.info('{} table dropped successfully.'.format(table_name))
        return len(list(cursor))

    @staticmethod
    def do_create_table_index(transaction_executor, table_name, index_attribute):
        logger.info("Creating index on '{}'...".format(index_attribute))
        statement = 'CREATE INDEX on {} ({})'.format(table_name, index_attribute)
        cursor = transaction_executor.execute_statement(statement)
        return len(list(cursor))

    @staticmethod
    def do_delete_ledger(ledger_name):
        logger.info('Attempting to delete the ledger with name: {}...'.format(ledger_name))
        result = qldb.client().delete_ledger(Name=ledger_name)
        logger.info('Success.')
        return result
