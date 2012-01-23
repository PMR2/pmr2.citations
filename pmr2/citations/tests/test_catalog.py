import unittest

import zope.component
import zope.interface

from pmr2.citations.interfaces import ICitation
from pmr2.citations.catalog import *

from pmr2.citations.tests.base import TestCitation


class CatalogIndexTestCase(unittest.TestCase):

    def setUp(self):
        obj = TestCitation('testobj')
        obj.ids = [u'urn:example:123', u'urn:test:123']
        obj.title = u'Test title'
        obj.creator = [u'Test A', u'Tester BA']
        self.obj = obj

    def tearDown(self):
        pass

    def test_0001_catalog_id(self):
        result = pmr2_citations_id(self.obj)()
        self.assertEqual(result, self.obj.ids)

    def test_0003_catalog_creator(self):
        result = pmr2_citations_creator(self.obj)()
        self.assertEqual(result, [u'Test', u'Tester'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CatalogIndexTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()

