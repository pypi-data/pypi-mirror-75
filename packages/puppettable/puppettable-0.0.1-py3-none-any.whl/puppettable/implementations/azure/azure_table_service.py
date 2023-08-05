from puppettable.implementations.azure.azure_table_stub_dictionary import AzureTableStubDictionary
from puppettable.implementations.azure.azure_table_stub_indexed import AzureTableStubIndexed
from puppettable.interface.table_service import TableService
from azure.cosmosdb.table import TableService as TableServiceSDK


class AzureTableService(TableService):

    TABLE_PROTOTYPES = {
        [].__class__.__name__: AzureTableStubIndexed,
        {}.__class__.__name__: AzureTableStubDictionary,
    }

    def __init__(self, connection_string):
        super().__init__()
        self._table_service = TableServiceSDK(connection_string=connection_string)

    @property
    def service(self):
        return self._table_service

    def __getitem__(self, table_name):
        table_proto_key = {}.__class__.__name__

        if type(table_name) is slice:
            table_proto_key = table_name.stop if type(table_name.stop) is str else table_name.stop.__class__.__name__
            table_name = table_name.start

        return self.TABLE_PROTOTYPES[table_proto_key](self, table_name)

    def __delitem__(self, table_name):
        self[table_name].delete()

    def __iter__(self):
        for table in self._table_service.list_tables():
            yield table.name

    def __len__(self):
        return len([n for n in self])

    def __str__(self):
        return "Azure " + super().__str__()
