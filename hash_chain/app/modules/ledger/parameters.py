from flask_restx import reqparse, inputs

from hash_chain.app.extensions.app_config import config
from hash_chain.app.modules.ledger.ddl.services import DdlServices


def ledger_name_parser_plain(default=config.LEDGER_NAME, parser=None, location='form'):
    help_text = 'Ledger name (default: "{}")'.format(default) if default else 'Ledger name'
    parser = reqparse.RequestParser() if not parser else parser
    parser.add_argument('ledger_name', type=inputs.regex('(?!^.*--)(?!^[0-9]+$)(?!^-)(?!.*-$)^[A-Za-z0-9-]+$'),
                        help=help_text,
                        location=location,
                        default=default, required=True, case_sensitive=True, trim=True)
    return parser


def ledger_name_parser_choices(default=config.LEDGER_NAME, parser=None, location='form'):
    parser = reqparse.RequestParser() if not parser else parser
    ledgers = DdlServices.ledger_list()
    choices = []
    for ledger in ledgers:
        if ledger.get('State') == config.ACTIVE_STATE:
            choices.append(ledger.get('Name'))

    parser.add_argument('ledger_name', choices=choices,
                        help='Ledger name',
                        location=location,
                        default=default, required=True, nullable=False, case_sensitive=True, trim=True)
    return parser


def ledger_name_parser_choices_or_plain(default=config.LEDGER_NAME, parser=None, location='form'):
    parser = reqparse.RequestParser() if not parser else parser
    try:
        parser = ledger_name_parser_choices(default=default, parser=parser, location=location)
    except Exception as e:
        parser = ledger_name_parser_plain(default, parser=parser, location=location)

    return parser


def table_name_parser_plain(default=config.LEDGER_NAME, parser=None, location='form'):
    parser = reqparse.RequestParser() if not parser else parser
    parser = ledger_name_parser_choices_or_plain(default=default, parser=parser, location=location)

    parser.add_argument('table_name', type=inputs.regex('^[A-Za-z_]{1}[A-Za-z0-9_]{1,127}$'),
                        help='A valid QLDB table name',
                        location=location,
                        default=None, required=True, nullable=False, case_sensitive=True, trim=True)
    return parser


def table_index_parser_plain(default=config.LEDGER_NAME, parser=None, location='form'):
    parser = reqparse.RequestParser() if not parser else parser
    parser = table_name_parser_plain(default=default, parser=parser, location=location)

    parser.add_argument('index_attribute', type=inputs.regex('^[A-Za-z_]{1}[A-Za-z0-9_]{1,127}$'),
                        help='The table field name on which to create the index.',
                        location=location,
                        default=None, required=True, nullable=False, case_sensitive=True, trim=True)
    return parser
