"""
Module providing cache-management utilities
"""

from collections import OrderedDict
from contextlib import contextmanager
import os
import shutil


class Cache:
    """
    Class managing a simple file-based cache, meant to be used by a single owner
    """

    def __init__(self, path: str, max_entries: int):
        self.cache_root = path
        self.max_entries = max_entries
        self.entries = OrderedDict()

    def _entry_path(self, name: str) -> str:
        return os.path.join(self.cache_root, name)

    def remove_entry(self, name: str):
        if self.has_entry(name):
            entry_path = self._entry_path(name)
            shutil.rmtree(entry_path, ignore_errors=True)

    @contextmanager
    def add_entry(self, name: str) -> str:
        entry_path = self._entry_path(name)
        os.makedirs(entry_path, mode=0o775, exist_ok=True)
        if name in self.entries:
            self.entries.move_to_end(name)
        else:
            if len(self.entries) == self.max_entries:
                evicted, _ = self.entries.popitem(last=False)
                self.remove_entry(evicted)
            self.entries[name] = None
        try:
            yield entry_path
        finally:
            pass

    def get_entry(self, name: str) -> str:
        if not self.has_entry(name):
            raise FileNotFoundError(name)
        self.entries.move_to_end(name)
        return self._entry_path(name)

    def has_entry(self, name: str) -> bool:
        return os.path.exists(self._entry_path(name))

    @staticmethod
    def from_directory(path: str, *, max_entries: int) -> 'Cache':
        return Cache(path, max_entries)

    @staticmethod
    def create_at(path: str, *, max_entries: int, exist_ok=False) -> 'Cache':
        os.makedirs(path, mode=0o775, exist_ok=exist_ok)
        return Cache.from_directory(path, max_entries=max_entries)
