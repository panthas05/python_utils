"""
A simple lockfile implementation, see:
https://stackoverflow.com/questions/6931342/system-wide-mutex-in-python-on-linux

Written for a context where a lock needs to be created which will lock processes
that weren't spawned by the process creating the lock. As such, implements
locking using the shared filesystem and fcntl (meaning this implementation only
works on Linux).
"""

import fcntl
import os
import threading
from typing import ClassVar, Type
from types import TracebackType

tmp_directory_path = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "tmp",
    )
)

# separate locks are needed for threads and processes
thread_locks: dict[str, threading.Lock] = {}


class InterProcessLock:

    def __init__(
        self,
        lock_specifier: str,
        timeout: int = -1,
    ) -> None:
        self.lock_specifier = lock_specifier
        if lock_specifier not in thread_locks:
            thread_locks[lock_specifier] = threading.Lock()
        self.timeout = timeout

    @property
    def lock_file_path(self) -> str:
        return os.path.join(
            tmp_directory_path,
            f"{self.lock_specifier}-lockfile.lck",
        )

    def __enter__(self) -> None:
        thread_locks[self.lock_specifier].acquire(
            timeout=self.timeout,
        )
        if not os.path.exists(self.lock_file_path):
            # create lockfile if doesn't exist yet
            open(self.lock_file_path, "x").close()
        self.file_instance = open(self.lock_file_path)
        fcntl.flock(
            self.file_instance.fileno(),
            fcntl.LOCK_EX,
        )

    def __exit__(
        self,
        exception_type: Type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType,
    ) -> bool | None:
        fcntl.flock(self.file_instance.fileno(), fcntl.LOCK_UN)
        self.file_instance.close()
        thread_locks[self.lock_specifier].release()
        if exception_type is not None:
            return False
        return None
