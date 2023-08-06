from cryptomodel.operations import OPERATIONS


class Repository:

    def __init__(self):
        self.memories = []

    def commit(self):
        for mem in self.memories:
            for item in mem.items:
                if item.operation == OPERATIONS.ADDED.name:
                    trans = mem.on_add(item)
                    if trans is not None:
                        item.id = trans.id
                elif item.operation == OPERATIONS.MODIFIED.name:
                    trans = mem.on_edit(item)
                    if trans is not None:
                        item.id = trans.id
                elif item.operation == OPERATIONS.REMOVED.name:
                    mem.on_remove(item, False)



