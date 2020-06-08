from http import HTTPStatus

from hash_chain.app.extensions import qldb
from hash_chain.app.extensions.logging import logger
from hash_chain.app.modules.ledger.core.utils import convert_object_to_ion, get_document_ids_from_dml_results
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
