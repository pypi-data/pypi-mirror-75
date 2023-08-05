from contextlib import redirect_stderr
from puppettable.interface.table_stub import TableStub
from azure.common import AzureMissingResourceHttpError


class AzureTableStub(TableStub):
    MAX_ENTITY_SIZE_BYTES = 523916
    MAX_BATCH_SIZE_BYTES = 4185932

    def __init__(self, owner, name):
        super().__init__(owner, name)
        self._partition = "default"
        self._progresses = []

    def exists(self):
        with redirect_stderr(None) as err:
            try:
                self._service.get_table_acl(self.name)
                result = True
            except AzureMissingResourceHttpError as e:
                result = False
        return result

    def create(self):
        """
        Forces the creation of this table in Azure.
        :return:
        """
        with redirect_stderr(None) as err:
            self._service.create_table(self.name)

    def delete(self):
        """
        Deletes this table from Azure.
        :return:
        """
        with redirect_stderr(None) as err:
            self._service.delete_table(self.name)

    def set_partition(self, partition_name="default"):
        """
        Sets the partition to the given name.
        :param partition_name:
        :return:
        """
        self._partition = partition_name
        self._stored_len = None

    @property
    def partition(self):
        return self._partition

    def __str__(self):
        return f"Table: '{super().__str__()}'; Partition: '{self.partition}'; Unknown length and size."

    def __repr__(self):
        return str(self)

    def sync(self, verbosity=2):
        """
        Waits for table being populated.
        """
        for progress in self._progresses:
            progress.wait(verbosity=verbosity)

        self._progresses = []

    def _batch(self):
        return self._service.batch(self._name)
