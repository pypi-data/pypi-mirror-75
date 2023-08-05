"""
This is the Azure table storage for not-indexed elements.

Allows to store any kind of element into the table storage (within the limits of Azure).
The elements can be sorted in any way. For example, this kind of table is perfect to store dictionary-like elements
(indexed by a string, for example).

Contrary to the indexed table, this is *not* able to track the size and the length of each of the tables it creates.
"""

import pandas as pd
import numpy as np

from puppettable.implementations.azure.azure_table_stub import AzureTableStub
from puppettable.implementations.azure.progress.update_progress import UpdateProgress
from contextlib import redirect_stderr

from puppettable.utils.azure_decorators import retry
from puppettable.utils.azure_parsers import parse_entity, generate_entity, parse_elements, build_elements

from azure.common import AzureMissingResourceHttpError


class AzureTableStubDictionary(AzureTableStub):

    def __init__(self, owner, name):
        super().__init__(owner, name)

    def __iter__(self):
        yield from self.query(None)

    def __getitem__(self, index):
        try:
            elements = self.get_raw(index)
            parsed_elements = parse_elements(elements)
        except AzureMissingResourceHttpError:
            raise KeyError(f"Index '{index}' not found.") from None

        return parsed_elements

    @retry(max_retries=1, recalculate_length=False)
    def __delitem__(self, index):

        if type(index) is list:
            self.delete_many(index)

        elif type(index) is slice:
            raise KeyError("Slice operation not supported on deletion.")

        else:
            index = str(index)
            self._service.delete_entity(self.name, self.partition, index)

    def delete_many(self, index_list):
        with self._service.batch(self.name) as b:
            for index in index_list:
                b.delete_entity(self.partition, index)

    def get_raw(self, index):
        if type(index) is list:
            result = [element for element in self.get_many(index)]

        elif type(index) is slice:
            queries = []

            if index.start is not None:
                queries.append(f"RowKey ge '{index.start}'")

            if index.stop is not None:
                queries.append(f"RowKey lt '{index.stop}'")

            query = " and ".join(queries)

            result = [element for element in self.query_raw(query)]

        else:
            result = parse_entity(self._service.get_entity(self.name, self.partition, str(index)))

        return result

    def query_raw(self, query):
        query = " and ".join([statement for statement in [f"PartitionKey eq '{self.partition}'", query] if statement is not None])

        for entity in self._service.query_entities(self.name, filter=query):
            yield parse_entity(entity)

    def query(self, query):
        for element in self.query_raw(query):
            yield element['X']

    @retry(max_retries=3, recalculate_length=False)
    def insert(self, data, index=-1, metadata=None):
        if metadata is None:
            metadata = {}

        row_key = str(index)

        entity, entity_size = generate_entity(data, self.partition, row_key=row_key, metadata=metadata)

        if entity_size > self.MAX_ENTITY_SIZE_BYTES:
            raise Exception(f"Entity too big ({entity_size}). Max allowed size is {self.MAX_ENTITY_SIZE_BYTES}")

        with redirect_stderr(None):
            self._service.insert_entity(self.name, entity)

        return entity_size

    def insert_many(self, indexes, data_list):
        return self.update_many(indexes, data_list)

    def update_many(self, indexes, data_list):
        indexes = pd.Index([str(x) for x in indexes], name="Index")

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

    @retry(max_retries=3, recalculate_length=False)
    def update(self, index, data, metadata=None):
        if metadata is None:
            metadata = {}

        if type(index) is list:
            if type(data) not in [list, np.ndarray, pd.DataFrame] or len(data) != len(index):
                raise ValueError(f"Expected a list of {len(index)} elements as values.")

            progress = self.update_many(index, data)

        elif type(index) is slice:
            raise KeyError("Updating slices is not supported in dictionary tables. Specify indexes as a list")

        else:
            index = str(index)

            if len(metadata) == 0:
                elements, metadata = build_elements(data, single_element=True)
                data = elements

            entity, entity_size = generate_entity(data, self.partition, row_key=index, metadata=metadata)
            self._service.insert_or_replace_entity(self.name, entity)
            progress = entity_size

        return progress

    @retry(max_retries=3, recalculate_length=False)
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

    def __str__(self):
        return f"Dictionary {super().__str__()}"
