import unittest

from .. import warntoexc
from ...storage import createStorage


setUpModule = warntoexc


class TestCreateStorage(unittest.TestCase):

  def testCreateStorageInvalid(self):
    with self.assertRaises(ValueError) as ctx:
      createStorage(None)
    self.assertEqual('Empty storage DSN', str(ctx.exception))

