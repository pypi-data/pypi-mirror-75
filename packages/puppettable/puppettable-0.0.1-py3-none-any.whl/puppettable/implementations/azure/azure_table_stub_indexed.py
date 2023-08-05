"""
This is the Azure table storage for indexed elements.

Allows to store any kind of element into the table storage (within the limits of Azure).
The elements must be sorted in a numeric way. For example, this kind of table is perfect to store numpy arrays,

It is able to track the size and the length of each of the tables
"""
import pandas as pd
import numpy as np
from azure.common import AzureMissingResourceHttpError

from puppettable.implementations.azure.azure_table_stub import AzureTableStub
from puppettable.implementations.azure.progress.update_progress import UpdateProgress
from contextlib import redirect_stderr
from puppettable.utils import numerize
from puppettable.utils.azure_decorators import ensure_length, retry
from puppettable.utils.azure_parsers import parse_entity, generate_entity, parse_elements, build_elements


def is_rowkey(index):
    try:
        integer_value = int(index)
        result = len(index) >= len(str(integer_value))
    except ValueError:
        result = False
    return result



class AzureTableStubIndexed(AzureTableStub):

    def __init__(self, owner, name):
        super().__init__(owner, name)

        self._stored_len = 0

        if self.exists():
            self._update_length()

    def __iter__(self):
        yield from self.query("")

    def size(self):
        """
        Estima el tamaño en Bytes. Es una estimación.
        """
        if not self.exists():
            return -1

        length = len(self)

        if length == 0:
            return 0

        first = 0
        for i in self._service.query_entities(self.name, f"PartitionKey eq '{self.partition}'", num_results=1):
            first = i
            break

        bytes_count = len("".join([str(first[x]) for x in first if x.startswith("X_")]).encode("utf-8")) if first != 0 else 0
        return bytes_count * length

    def _find_min_max(self, exp=20):

        for i in range(exp):
            n = 10 ** i - 1

            f = f"PartitionKey eq '{self.partition}' and (RowKey eq '{numerize(n)}' or RowKey gt '{numerize(n)}')"
            len_elements = len(list(self._service.query_entities(self.name, filter=f, num_results=1, select='RowKey')))

            if len_elements == 0:
                if n == 0:
                    n += 1
                return max(n // 10, 0), n

        return 0, 1

    def _find_max(self, known_min=0, range_size=10, known_max=10000000, max_depth=30, level=0):

        if level >= max_depth:
            raise Exception(f"Max depth ({max_depth}) reached (known_min: {known_min}; known_max: {known_max})")

        if known_min == known_max:
            return known_min

        mean_point = (known_min + known_max) // 2

        f = f"PartitionKey eq '{self.partition}' and (RowKey gt '{numerize(mean_point)}' or RowKey eq '{numerize(mean_point)}')"
        elements = [int(element["RowKey"]) for element in
                    self._service.query_entities(self.name, filter=f, num_results=range_size, select='RowKey')]
        len_elements = len(elements)

        if len_elements == range_size:
            known_min = max(elements)

        elif 0 < len_elements < range_size:
            known_min = max(elements)
            known_max = known_min

        elif len_elements == 0:
            known_max = mean_point
            if known_min == known_max == 0:
                known_min = known_max = -1

        return self._find_max(known_min, range_size, known_max, max_depth, level + 1)

    def _update_length(self):
        """
        Busca el elemento máximo de forma óptima (iterando lo menos posible).
        Normalmente lo encuentra en menos de 20 iteraciones.
        """
        min_v, max_v = self._find_min_max()
        max_v = self._find_max(known_min=min_v, known_max=max_v)

        self._stored_len = max_v + 1

    def __str__(self):
        size = format(round(self.size() / 1024, 2), ',').replace(',', 'a').replace('.', ',').replace("a", ".")
        return f"Indexed Table: '{super().__str__()}'; Partition: '{self.partition}'; Length: {len(self)}; Size: {size} KB"

    def __len__(self):
        if self._stored_len is None and self.exists():
            self._update_length()

        return self._stored_len

    def __getitem__(self, index):
        try:
            elements = self.get_raw(index)
            parsed_elements = parse_elements(elements)

        except AzureMissingResourceHttpError as e:
            raise KeyError(f"Index '{index}' not found.")

        return parsed_elements

    @retry(max_retries=1)
    def __delitem__(self, index):

        if type(index) is list:
            self.delete_many(index)

        elif type(index) is str:
            raise KeyError("String as index not supported.")

        elif type(index) is int:
            length = len(self)
            if index >= length:
                raise KeyError(f"Index {index} out of bounds ({length}).")
            index = index % length
            self._service.delete_entity(self.name, self.partition, numerize(index))

        elif type(index) is slice:
            length = len(self)
            min_value = 0 if index.start is None else length + index.start if index.start < 0 else index.start
            max_value = max(length if index.stop is None else length + index.stop if index.stop < 0 else index.stop,
                            length - 1)
            step = index.step or 1

            if step < 0:
                raise Exception("Reverse order not supported.")

            self.delete_many([i for i in range(min_value, max_value, step)])
        else:
            raise KeyError(f"Index '{index}' format not supported.")

        self._stored_len = None

    def delete_many(self, index_list):
        with self._service.batch(self.name) as b:
            for i in index_list:
                b.delete_entity(self.partition, numerize(i))

    def get_raw(self, index):
        length = len(self)

        if type(index) is list:
            result = [element for element in self.get_many(index)]

        elif type(index) is slice:
            min_value = 0 if index.start is None else length + index.start if index.start < 0 else index.start
            max_value = length if index.stop is None else length + index.stop if index.stop < 0 else index.stop
            step = index.step or 1

            if step < 0:
                raise Exception("Reverse order not supported.")

            queries = []

            if min_value is not None:
                queries.append(f"RowKey gt '{numerize(min_value - 1)}'")

            if max_value is not None:
                queries.append(f"RowKey lt '{numerize(max_value)}'")

            query = " and ".join(queries)

            elements = self.query_raw(query)

            result = [element for i, element in enumerate(elements) if i % step == 0]

        elif type(index) is int:
            if index < length:
                #raise KeyError(f"Index '{index}' out of bounds ({length}).")
                index = index % length

            result = parse_entity(self._service.get_entity(self.name, self.partition, numerize(index)))

        elif type(index) is str and is_rowkey(index):
            result = parse_entity(self._service.get_entity(self.name, self.partition, index))

        else:
            raise KeyError(f"Key '{index}' format not supported. Only lists, slices or integer values are supported.")

        return result

    def query_raw(self, query):
        query = " and ".join([statement for statement in [f"PartitionKey eq '{self.partition}'", query] if statement is not None])

        for entity in self._service.query_entities(self.name, filter=query):
            yield parse_entity(entity)

    def query(self, query):
        for element in self.query_raw(query):
            yield element['X']

    @ensure_length
    @retry(max_retries=3)
    def insert(self, data, index=-1, metadata=None):
        if metadata is None:
            metadata = {}

        if index == -1:
            row_key = numerize(len(self))
        else:
            row_key = index

        entity, entity_size = generate_entity(data, self.partition, row_key=row_key, metadata=metadata)

        if entity_size > self.MAX_ENTITY_SIZE_BYTES:
            raise Exception(f"Entity too big ({entity_size}). Max allowed size is {self.MAX_ENTITY_SIZE_BYTES}")

        with redirect_stderr(None) as err:
            self._service.insert_entity(self.name, entity)

        if self._stored_len is None:
            self._update_length()
        self._stored_len += 1

        return self._stored_len - 1, entity_size

    def append(self, item):
        return self.insert(item)

    @ensure_length
    def append_many(self, data_list):
        length = len(self)

        indexes = pd.Index([numerize(x + length) for x in range(data_list.shape[0])], name="Index")

        return self.update_many(indexes, data_list)

    @ensure_length
    def update_many(self, indexes, data_list):
        indexes = pd.Index([numerize(x) for x in indexes], name="Index")

        elements, metadata = build_elements(data_list)
        data_list = pd.DataFrame(elements)
        data_list.index = indexes

        # This forces the creation of the table if it doesn't exist already
        if metadata.get("datatype", "unknown") == "unknown":
            size = self.update(index=data_list.iloc[0].name, data=data_list.iloc[0].values[0], metadata=metadata)
        elif metadata.get("datatype", "unknown") == "pandas_series":
            size = self.update(index=data_list.iloc[0].name, data=data_list.iloc[0], metadata=metadata)

        else:
            size = self.update(index=data_list.iloc[0].name, data=data_list.iloc[0].values, metadata=metadata)

        progress = UpdateProgress(self, data_list.iloc[1:], metadata=metadata)
        progress._total_elements = len(data_list)
        progress._total_uploaded_elements += 1
        progress._total_uploaded_bytes += size

        progress.start()
        self._progresses.append(progress)

        return progress

    @retry(max_retries=3)
    def update(self, index, data, metadata=None):
        if metadata is None:
            metadata = {}

        length = len(self)

        if type(index) is slice:
            min_value = 0 if index.start is None else length + index.start if index.start < 0 else index.start
            max_value = length if index.stop is None else length + index.stop if index.stop < 0 else index.stop
            step = index.step or 1

            segment_length = ((max_value or length) - (min_value or 0)) // step

            data_is_a_list = type(data) in [list, np.ndarray]

            if not data_is_a_list or len(data) != segment_length:
                raise ValueError(f"Expected a list of {segment_length} elements as values.")

            if step < 0:
                raise Exception("Reverse order not supported.")

            indexes = [i % length if i < 0 else i for i in range(min_value, max_value, step)]

            max_index = np.max(indexes)
            if max_index > len(self):
                self._stored_len = max_index + 1

            data_list = data

            progress = self.update_many(indexes, data_list)

        elif type(index) is list:
            if type(data) not in [list, np.ndarray, pd.DataFrame] or len(data) != len(index):
                raise ValueError(f"Expected a list of {len(index)} elements as values.")

            indexes = [i % length if i < 0 else i for i in index]

            max_index = np.max(indexes)
            if max_index > len(self):
                self._stored_len = max_index + 1

            data_list = data

            progress = self.update_many(indexes, data_list)
        elif type(index) is int:

            if index < 0:
                index = index % length

            if len(metadata) == 0:
                elements, metadata = build_elements(data, single_element=True)
                data = elements

            if index > len(self):
                self._stored_len = index + 1

            entity, entity_size = generate_entity(data, self.partition, row_key=numerize(index), metadata=metadata)
            self._service.insert_or_replace_entity(self.name, entity)
            progress = entity_size

        elif type(index) is str and is_rowkey(index):

            if len(metadata) == 0:
                elements, metadata = build_elements(data, single_element=True)
                data = elements

            entity, entity_size = generate_entity(data, self.partition, row_key=index, metadata=metadata)
            self._service.insert_or_replace_entity(self.name, entity)
            progress = entity_size

        else:
            raise KeyError(f"Key '{index}' format not supported. Only lists, slices or integer values are supported.")

        return progress

    @retry(max_retries=3)
    def __setitem__(self, index, data):
        progress = self.update(index, data)

        return progress

    # @retry(max_retries=3)
    def get_many(self, index_list):
        raise NotImplementedError("This operation is not supported by the backend.")
        # length = len(self)
        # with table_service.batch(self.name) as b:
        #    entities = [parse_entity(b.get_entity(self.name, self.partition, numerize(numerize(index))))['X'] if index < length else raise_(KeyError(f"Index {i} out of bounds ({length})")) for index in index_list]
        # return entities
