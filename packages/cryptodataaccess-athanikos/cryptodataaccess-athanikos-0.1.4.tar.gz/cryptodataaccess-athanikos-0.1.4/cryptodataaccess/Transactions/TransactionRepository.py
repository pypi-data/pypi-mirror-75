from cryptomodel.cryptostore import user_transaction, OPERATIONS

from cryptodataaccess.Memory import Memory
from cryptodataaccess.Repository import Repository


class TransactionRepository(Repository):

    def __init__(self, transaction_store):
        self.transaction_store = transaction_store
        self.transactions = []
        super(TransactionRepository, self).__init__()
        memory = Memory(on_add=self.transaction_store.insert_transaction,
                        on_edit=self.transaction_store.update_transaction,
                        on_remove=self.transaction_store.delete_transaction,
                        items=self.transactions
                        )
        self.memories.append(memory)

    def get_distinct_user_ids(self):
        return self.transaction_store.fetch_distinct_user_ids()

    def get_transaction(self, id):
        return self.transaction_store.fetch_transaction(id)

    def get_transactions(self, user_id):
        return self.transaction_store.fetch_transactions(user_id)

    def add_transaction(self, user_id, volume, symbol, value, price, currency, date, source, source_id):
        self.transactions.append(
            user_transaction(user_id=user_id, volume=volume, symbol=symbol, value=value, price=price,
                             currency=currency, date=date, source=source, source_id=source_id,
                             operation=OPERATIONS.ADDED.name))

    def edit_transaction(self, in_id, user_id, volume, symbol, value, price, currency, date, source, source_id):
        self.transactions.append(
            user_transaction(id=in_id,
                             user_id=user_id, volume=volume, symbol=symbol, value=value, price=price,
                             currency=currency, date=date, source=source, source_id=source_id,
                             operation=OPERATIONS.MODIFIED.name))

    def remove_transaction(self, in_id):
        trans = next((x for x in self.transactions if x.id == in_id), None)
        self.mark_deleted(trans)

    def remove_transaction_by_source_id(self, source_id, throw_if_does_not_exist=True):
        trans = next((x for x in self.transactions if x.source_id == source_id), None)
        self.mark_deleted(trans)

    def mark_deleted(self, trans):
        if trans is None:
            trans = self.get_transaction(id)
            trans.operation = OPERATIONS.REMOVED.name
            self.transactions.append(trans)
        else:
            trans.operation = OPERATIONS.REMOVED.name
