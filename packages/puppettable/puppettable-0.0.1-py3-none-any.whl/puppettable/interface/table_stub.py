class TableStub:

    def __init__(self, owner, name):
        self._owner = owner
        self._name = name
        self._service = owner.service

    def __str__(self):
        return self._name

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self._name

    def exists(self):
        raise NotImplementedError("Not implemented")

    def delete(self):
        raise NotImplementedError("Not implemented")

    def __len__(self):
        raise NotImplementedError("Not implemented")

    def size(self):
        raise NotImplementedError("Not implemented")

    def insert(self, element, index=-1, metadata=None):
        raise NotImplementedError("Not implemented")

    def append_many(self, items):
        raise NotImplementedError("Not implemented")

    def __setitem__(self, key, value):
        raise NotImplementedError("Not implemented")

    def update_many(self, indexes, items):
        raise NotImplementedError("Not implemented")

    def __delitem__(self, key):
        raise NotImplementedError("Not implemented")

    def delete_many(self, items):
        raise NotImplementedError("Not implemented")

    def __getitem__(self, item):
        raise NotImplementedError("Not implemented")

    def get_many(self, items):
        raise NotImplementedError("Not implemented")

    def set_partition(self, partition_name):
        raise NotImplementedError("Not implemented")

    def __iter__(self):
        raise NotImplementedError("Not implemented")
