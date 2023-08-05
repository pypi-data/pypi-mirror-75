class TableService:

    def __getitem__(self, table_name):
        raise NotImplementedError("Not Implemented")

    def __delitem__(self, table_name):
        raise NotImplementedError("Not Implemented")

    def __iter__(self):
        raise NotImplementedError("Not Implemented")

    def __str__(self):
        table_names = [x for x in self]
        length = len(table_names)
        string = f"{length} Tables: [" + ", ".join([f'"{n}"' for n, i in zip(table_names, range(3))]) + (
            f', ..., "{table_names[-1]}"' if length > 4 else f', "{table_names[-1]}"' if length == 4 else "") + "]"
        return string

    def __repr__(self):
        return str(self)

    def __len__(self):
        raise NotImplementedError("Not Implemented")
