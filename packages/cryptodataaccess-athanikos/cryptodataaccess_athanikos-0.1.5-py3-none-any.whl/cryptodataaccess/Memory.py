"""
Represents an item list contained within Repository
keeps the set of methods executed for add/edit/delete
"""


class Memory:

    def __init__(self, on_add, on_edit, on_remove, items):
        self.on_add = on_add
        self.on_remove = on_remove
        self.on_edit = on_edit
        self.items = items