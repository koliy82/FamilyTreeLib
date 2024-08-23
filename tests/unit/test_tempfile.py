import os
import unittest

from familytreelib import TempFile


class TempFileTest(unittest.TestCase):

    def test_temp_file_create(self):
        with TempFile(suffix=".png") as file:
            self.assertTrue(os.path.exists(file.path))

    def test_temp_file_read(self):
        with TempFile(suffix=".png") as file:
            file.temp_file.write(b"test")
            file.temp_file.seek(0)
            self.assertEqual(file.temp_file.read(), b"test")

    def test_temp_file_delete(self):
        with TempFile(suffix=".png") as file:
            self.assertTrue(os.path.exists(file.path))
        self.assertFalse(os.path.exists(file.path))