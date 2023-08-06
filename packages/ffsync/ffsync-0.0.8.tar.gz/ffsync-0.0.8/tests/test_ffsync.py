"""Tests for the sync2vids.sync module."""

from unittest import TestCase
from ffsync import sync

class TestConsole(TestCase):
    def test_basic(self):
        sync.sync('tests/tests_files/sync.csv', 'tests/tests_files')
