import unittest

from pySpack.pyspack import PySpack


class Test_TestPySpack(unittest.TestCase):
    def setUp(self):
        self.pyspack = PySpack()

    def test_install(self):
        self.assertTrue(self.pyspack.install('py-json5'))

    def test_is_installable(self):
        self.assertTrue(self.pyspack.is_installable('py-json5'))

    def test_find(self):
        self.pyspack.install('py-json5')
        self.assertTrue(self.pyspack.find('py-json5'))

    def test_not_found(self):
        self.pyspack.uninstall('py-json5')
        self.assertFalse(self.pyspack.find('py-json5'))

    def test_uninstall(self):
        self.pyspack.install('py-json5')
        
        self.assertTrue(self.pyspack.uninstall('py-json5'))
