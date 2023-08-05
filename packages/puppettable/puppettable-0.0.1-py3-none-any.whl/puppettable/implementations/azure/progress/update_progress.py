from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import Thread

from puppettable.implementations.azure.progress import AzureProgress
from puppettable.utils.azure_parsers import generate_entity


class UpdateProgress(AzureProgress):

    def __init__(self, owner, elements=None, metadata=None):
        super().__init__(owner, elements=elements, metadata=metadata)

        self._queue_processor = Thread(target=self._process_queue, name="QueueProcessor")
        self._partition = owner.partition
        self._pool = None

    def _make_batch(self):
        """
        Makes a new batch from the elements based on the Azure's limits.

        :return: Tuple: [row_key for each element of the batch, batch of elements, size of batch in Bytes]
        """
        row_keys = []
        entities = []
        sizes = []

        batch = None

        unqueued_elements = self._remaining_elements.query("queued == 0").iloc[:self.HARD_MAX_BATCH_SIZE_ELEMENTS, :-1]

        for row_key, data in unqueued_elements.iterrows():
            if self._metadata.get("datatype", "unknown") == "unknown":
                entity, size = generate_entity(data.values[0], self._partition, row_key=row_key, metadata=self._metadata)
            elif self._metadata.get("datatype", "unknown") == "pandas_series":
                entity, size = generate_entity(data, self._partition, row_key=row_key, metadata=self._metadata)
            else:
                entity, size = generate_entity(data.values, self._partition, row_key=row_key, metadata=self._metadata)

            if sum(sizes) + size > self.HARD_MAX_BATCH_SIZE_BYTES:
                break
            else:
                row_keys.append(row_key)
                entities.append(entity)
                sizes.append(size)

        if batch is None:
            batch = (row_keys, entities, sizes)

        queued_elements = unqueued_elements.iloc[:len(row_keys)]
        with self._lock:
            self._remaining_elements_to_queue -= len(row_keys)
            self._remaining_elements.loc[queued_elements.index, "queued"] = 1

        return batch

    def _upload_batch(self, batch):
        row_keys, entities, sizes = batch

        with self._owner._batch() as b:  # Demeter's law... :'(
            for entity in entities:
                b.insert_or_replace_entity(entity)

        return batch

    def _make_promise(self, batch):
        promise = self._pool.submit(self._upload_batch, batch)
        return promise

    def _refill_queue(self):
        # We build batches and append them to the queue.
        while self._queue_hungry():
            new_batch = self._make_batch()
            batch_promise = self._make_promise(new_batch)

            with self._lock:
                self._batch_promises_queue.append(batch_promise)

    def _update_stats(self, batch):
        batch_elements_length = len(batch[1])
        batch_bytes_size = batch[2]

        with self._lock:
            self._total_uploaded_bytes += sum(batch_bytes_size)
            self._total_uploaded_elements += batch_elements_length

    def _remove_completed(self, promise, batch):
        row_keys = batch[0]

        with self._lock:
            self._batch_promises_queue.remove(promise)
            self._remaining_elements.drop(row_keys)

    def _process_queue(self):

        while not self.finished():

            # We ensure the queue is filled everytime.
            try:
                self._refill_queue()

                for i, promise in enumerate(as_completed(self._batch_promises_queue)):
                    batch = promise.result()

                    self._update_stats(batch)
                    self._remove_completed(promise, batch)

                    self.progress_callback()

                    if self.aborted():
                        raise Exception("Aborted.")

                    # We force a refill in the half of the promise process.
                    if i == self.SOFT_MIN_BATCH_QUEUE_SIZE // 2:
                        break

            except Exception as e:
                with self._lock:
                    self._error = e

                self._pool.shutdown(wait=False)
                raise e

    def start(self):
        """
        Enables the queue and process threads for insertions.
        :return:
        """
        self._pool = ThreadPoolExecutor(4)
        self._queue_processor.start()
