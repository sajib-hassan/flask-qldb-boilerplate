from hash_chain.app.extensions import qldb
from hash_chain.app.extensions.app_config import config
from hash_chain.app.extensions.logging import logger
from hash_chain.app.modules.ledger.ddl.services import DdlServices
from hash_chain.app.modules.ledger.helpers import wait_for_active, set_deletion_protection, wait_for_deleted


class Migration(object):

    def __init__(self):
        self.ledger_name = config.LEDGER_NAME
        self.hash_table_name = config.HASH_TABLE_NAME

    def migrate(self, direction='UP'):
        if direction == 'DOWN':
            self.down()
        elif direction == 'UP':
            self.up()
        else:
            logger.info('Direction is missing!')

    def up(self):
        try:
            self.create_ledger()
            if self.table_exist():
                logger.info('Table already exist!')
                return True
            self.create_table()
            self.create_table_indexes(['service_id', 'document_id', 'document_hash', 'field_list', 'op_mode'])
        except Exception as e:
            logger.exception('Migration UP failed! {}.'.format(e))

    def down(self):
        try:
            self.drop_table()
            self.drop_ledger()
        except Exception as e:
            logger.exception('Migration DOWN failed! {}.'.format(e))

    def create_ledger(self):
        """Create a ledger and wait for it to be active."""
        if self.ledger_exist():
            logger.info('Ledger already exist!')
            return True

        DdlServices.do_create_ledger(self.ledger_name)
        wait_for_active(self.ledger_name)
        DdlServices.reset_ledgers()

    def create_table(self):
        """Create a Table"""
        with qldb.session(self.ledger_name) as session:
            session.execute_lambda(lambda x: DdlServices.do_create_table(x, self.hash_table_name),
                                   lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Table created successfully.')

    def create_table_indexes(self, index_attributes=[]):
        """Create index on tables in a particular ledger."""
        logger.info('Creating index on all tables in a single transaction...')
        with qldb.session(self.ledger_name) as session:
            for index_attribute in index_attributes:
                session.execute_lambda(
                    lambda x: DdlServices.do_create_table_index(x, self.hash_table_name, index_attribute),
                    lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Index created successfully.')

    def drop_ledger(self):
        """Delete a ledger."""
        set_deletion_protection(self.ledger_name, False)
        DdlServices.do_delete_ledger(self.ledger_name)
        wait_for_deleted(self.ledger_name)
        DdlServices.reset_ledgers()

    def drop_table(self):
        """Create a Table"""
        with qldb.session(self.ledger_name) as session:
            session.execute_lambda(lambda x: DdlServices.do_drop_table(x, self.hash_table_name),
                                   lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Table dropped successfully.')

    def ledger_exist(self):
        """
        Returns information about a ledger, including its state and when it was created.
        """
        try:
            logger.info("Let's describe ledger...{}".format(self.ledger_name))
            ledger = qldb.client().describe_ledger(Name=self.ledger_name)
            logger.info('Success. describe ledger...{}.'.format(ledger))
            return ledger
        except Exception as e:
            logger.exception('Unable to list ledgers!')
            return None

    def table_exist(self):
        """
            Connect to a session for a given ledger using default settings.
            """
        try:
            qldb_session = qldb.session(self.ledger_name)
            logger.info('Listing table names ')
            tables = qldb_session.list_tables()
            _tables = []
            for table in tables:
                _tables.append(table)
            return self.hash_table_name in _tables
        except Exception as e:
            logger.exception('Unable to create session.')
            return False
