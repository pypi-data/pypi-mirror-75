from datetime import datetime
from threading import Lock
from time import sleep
import numpy as np
from tqdm.auto import tqdm


class Progress:
    def __init__(self, elements=None):
        if elements is None:
            elements = []

        self._remaining_elements = elements
        self._total_uploaded_elements = 0
        self._total_elements = len(elements)
        self._total_uploaded_bytes = 0

        self._error = None
        self._abort = False
        self._tqdm = None
        self._verbosity = 0
        self._lock = Lock()

    def abort(self):
        with self._lock:
            self._abort = True

    def errored(self):
        with self._lock:
            return self._error is not None

    def aborted(self):
        with self._lock:
            return self._abort

    @property
    def total_uploaded_elements(self):
        return self._total_uploaded_elements

    @property
    def total_uploaded_bytes(self):
        return self._total_uploaded_bytes

    @property
    def total_elements(self):
        return self._total_elements

    @property
    def resume_args(self):
        return (
        self._remaining_elements, self._total_uploaded_elements, self._total_elements, self._total_uploaded_bytes,
        self.progress_callback)

    def _tdqm_progress(self):
        if self._tqdm is None:
            self._tqdm = tqdm(dynamic_ncols=True, total=self._total_elements)
            self._tqdm.set_description(f"Total uploaded {self._total_uploaded_bytes/1024} KBytes")
            self._tqdm.update(self._total_uploaded_elements)
        return self._tqdm

    def finished(self):
        return self._total_uploaded_elements == self._total_elements or self.aborted() or self.errored()

    def wait(self, timeout=0, verbosity=1):
        wait_time_start = datetime.now()
        try:
            self._verbosity = verbosity

            def timedout():
                return (datetime.now() - wait_time_start).total_seconds() >= timeout and timeout > 0

            while not timedout() and not self.finished():
                sleep(0.5)

        except (KeyboardInterrupt, Exception) as e:
            self.abort()
            raise e

        finally:
            self._verbosity = 0

        if self.errored():
            raise self._error

    def progress_callback(self):
        if self._verbosity == 1:
            print(f"{self._total_uploaded_elements} / {self._total_elements}  ({self._total_uploaded_bytes} Bytes)")

        if self._verbosity == 2:
            tqdm_progress = self._tdqm_progress()
            tqdm_progress.n = self._total_uploaded_elements
            tqdm_progress.set_description(f"{self._total_uploaded_bytes} Bytes")
            tqdm_progress.refresh()

    def checkpoint(self, to_file):
        """
        Saves the progress to a file. It can be resumed afterwards-
        :param to_file: filename to store the checkpoint
        """
        ckpt = {
            "remaining_elements": self._remaining_elements,
            "total_uploaded_elements": self._total_uploaded_elements,
            "total_elements": self._total_elements,
            "total_uploaded_bytes": self._total_uploaded_bytes
        }

        np.save(to_file, ckpt)

    @classmethod
    def from_file(cls, from_file):
        ckpt = np.load(from_file, allow_pickle=True)[0]
        instance = cls()
        instance._remaining_elements = ckpt['remaining_elements']
        instance._total_uploaded_elements = ckpt['total_uploaded_elements']
        instance._total_elements = ckpt['total_elements']
        instance._total_uploaded_bytes = ckpt['total_uploaded_bytes']
