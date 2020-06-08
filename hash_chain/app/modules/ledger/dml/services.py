from http import HTTPStatus

from hash_chain.app.extensions import qldb
from hash_chain.app.extensions.logging import logger
from hash_chain.app.modules.ledger.core.utils import convert_object_to_ion, get_document_ids_from_dml_results, \
    parse_result
from hash_chain.app.util import success_response, fail_response


class DmlServices(object):
    ledgers = None

    @staticmethod
    def insert_documents(ledger_name, table_name, documents):
        """
            Insert documents into a table in a QLDB ledger.
            """
        try:
            with qldb.session(ledger_name) as session:
                # An INSERT statement creates the initial revision of a document with a version number of zero.
                # QLDB also assigns a unique document identifier in GUID format as part of the metadata.
                session.execute_lambda(
                    lambda executor: DmlServices.do_insert_documents(executor, table_name, documents),
                    lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                logger.info('Documents inserted successfully!')
                return success_response('Ledger is active and ready to use.', HTTPStatus.CREATED)
        except Exception as e:
            logger.exception('Error inserting or updating documents.')
            return fail_response('Error inserting or updating documents. error: {}. Please try again.'.format(e),
                                 HTTPStatus.UNPROCESSABLE_ENTITY)

    @staticmethod
    def get_table_data(ledger_name, table_name, where='1=1', limit=10, offset=0):
        """ Scan for all the documents in a table."""
        try:
            with qldb.session(ledger_name) as session:
                # Scan all the tables and print their documents.
                tables = session.list_tables()
                for table in tables:
                    cursor = session.execute_lambda(
                        lambda executor: DmlServices.scan_table(executor, table_name, where, limit, offset),
                        retry_indicator=lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
                    logger.info('Scan successful!')
                    return parse_result(cursor)
        except Exception as e:
            logger.exception('Unable to scan tables. {}'.format(e))

    @staticmethod
    def do_insert_documents(transaction_executor, table_name, documents):
        """
        Insert the given list of documents into a table in a single transaction.

        :type transaction_executor: :py:class:`pyqldb.execution.executor.Executor`
        :param transaction_executor: An Executor object allowing for execution of statements within a transaction.

        :type table_name: str
        :param table_name: Name of the table to insert documents into.

        :type documents: list
        :param documents: List of documents to insert.

        :rtype: list
        :return: List of documents IDs for the newly inserted documents.
        """
        logger.info('Inserting some documents in the {} table...'.format(table_name))
        statement = 'INSERT INTO {} ?'.format(table_name)
        cursor = transaction_executor.execute_statement(statement, convert_object_to_ion(documents))
        list_of_document_ids = get_document_ids_from_dml_results(cursor)

        return list_of_document_ids

    @staticmethod
    def scan_table(transaction_executor, table_name, where='1=1', limit=10, offset=0):
        """
        Scan for all the documents in a table.

        :type transaction_executor: :py:class:`pyqldb.execution.executor.Executor`
        :param transaction_executor: An Executor object allowing for execution of statements within a transaction.

        :type table_name: str
        :param table_name: The name of the table to operate on.

        :type where: str
        :param where: where condition.

        :type limit: int
        :param limit: query result limit

        :type offset: int
        :param offset: query result offset.

        :rtype: :py:class:`pyqldb.cursor.stream_cursor.StreamCursor`
        :return: Cursor on the result set of a statement query.
        """
        logger.info('Scanning {}...'.format(table_name))
        # query = 'SELECT * FROM {table_name} WHERE {where} LIMIT {limit} OFFSET {offset}'.format(
        query = 'SELECT * FROM {table_name} WHERE {where}'.format(
            table_name=table_name,
            where=where,
            # limit=limit,
            # offset=offset
        )
        return transaction_executor.execute_statement(query)
