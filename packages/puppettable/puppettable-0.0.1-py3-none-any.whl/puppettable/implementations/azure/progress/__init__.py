import pandas as pd
from puppettable.utils.progress import Progress


class AzureProgress(Progress):
    HARD_MAX_ENTITY_SIZE_BYTES = 523916
    HARD_MAX_BATCH_SIZE_BYTES = 4185932
    HARD_MAX_BATCH_SIZE_ELEMENTS = 100

    SOFT_MIN_BATCH_QUEUE_SIZE = 200  # Internal limit of number of batches we keep in the batch buffer

    def __init__(self, owner, elements=None, metadata=None):
        if elements is None:
            elements = []

        if type(elements) is not pd.DataFrame:
            elements = pd.DataFrame(elements)
        else:
            elements = elements.copy()

        elements['queued'] = 0

        super().__init__(elements)
        self._metadata = metadata
        self._owner = owner
        self._batch_promises_queue = []
        self._remaining_elements_to_queue = len(elements)

    def _queue_hungry(self):
        with self._lock:
            return len(self._batch_promises_queue) < self.SOFT_MIN_BATCH_QUEUE_SIZE and \
                   len(self._remaining_elements) > 0 and  self._remaining_elements_to_queue > 0

