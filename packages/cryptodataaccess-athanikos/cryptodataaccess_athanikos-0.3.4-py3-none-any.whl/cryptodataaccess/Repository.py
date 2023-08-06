from cryptomodel.operations import OPERATIONS


class Repository:

    def __init__(self):
        self.memories = {}

    def commit(self):
        for key, mem in self.memories.items():
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

    """
    Assumes item has two attributes named as follows  
    operation  values : ADDED, REMOVED , MODIFIED 
    """

    def mark_deleted(self, memory_key, on_select, id_value, id_name):
        item = next((x for x in self.memories[memory_key].items if getattr(x, id_name) == id_value), None)
        if item is None:
            trans = on_select(id_value)
            if trans is None:
                exit
            else:
                trans.operation = OPERATIONS.REMOVED.name
                self.memories[memory_key] = item
        else:
            item.operation = OPERATIONS.REMOVED.name