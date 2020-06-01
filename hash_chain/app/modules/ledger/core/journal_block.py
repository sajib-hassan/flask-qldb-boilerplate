class JournalBlock:
    """
    Represents a JournalBlock that was recorded after executing a transaction in the ledger.
    """

    def __init__(self, block_address, transaction_id, block_timestamp, block_hash, entries_hash, previous_block_hash,
                 entries_hash_list, transaction_info, revisions):
        self.block_address = block_address
        self.transaction_id = transaction_id
        self.block_timestamp = block_timestamp
        self.block_hash = block_hash
        self.entries_hash = entries_hash
        self.previous_block_hash = previous_block_hash
        self.entries_hash_list = entries_hash_list
        self.transaction_info = transaction_info
        self.revisions = revisions


def from_ion(ion_value):
    """
    Construct a new JournalBlock object from an IonStruct.

    :type ion_value: :py:class:`amazon.ion.simple_types.IonSymbol`
    :param ion_value: The IonStruct returned by QLDB that represents a journal block.

    :rtype: :py:class:`hash_chain.ledger.qldb.journal_block.JournalBlock`
    :return: The constructed JournalBlock object.
    """
    block_address = ion_value.get('blockAddress')
    transaction_id = ion_value.get('transactionId')
    block_timestamp = ion_value.get('blockTimestamp')
    block_hash = ion_value.get('blockHash')
    entries_hash = ion_value.get('entriesHash')
    previous_block_hash = ion_value.get('previousBlockHash')
    entries_hash_list = ion_value.get('entriesHashList')
    transaction_info = ion_value.get('transactionInfo')
    revisions = ion_value.get('revisions')

    journal_block = JournalBlock(block_address, transaction_id, block_timestamp, block_hash, entries_hash,
                                 previous_block_hash, entries_hash_list, transaction_info, revisions)
    return journal_block
