from cStringIO import StringIO
from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from Products.PloneTestCase import PloneTestCase as ptc

from pmr2.citations.interfaces import ICitation
from pmr2.citations.utility import *
from pmr2.citations.content import Citation

#from pmr2.citations.tests.base import TestCitation


class CitationTestCase(ptc.PloneTestCase):
    """\
    The core citation test case.
    """

    def setUp(self):
        self.container = {}
        self.exporter = JsonCitationExporter()
        self.importer = JsonCitationImporter()

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_0000_json_import_export_cycle(self):
        testid = 'urn:test1'
        citation = Citation(testid)
        #citation.id = 'urn:test1'
        citation.title = u'Test Title One'
        citation.creator = ['Tester One', 'Tester Two']
        citation.issued = u'2001-01-01'
        citation.bibliographicCitation = u'Test Journal'
        citation.abstract = None

        self.container[citation.id] = citation
        jsonstr = self.exporter.export(self.container)
        jsonstream = StringIO(jsonstr)

        new_container = {}
        self.importer.parseInto(new_container, jsonstream)

        
        self.assertEqual(new_container[testid].id, 
                         self.container[testid].id)
        self.assertEqual(new_container[testid].title, 
                         self.container[testid].title)
        self.assertEqual(new_container[testid].creator, 
                         self.container[testid].creator)


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CitationTestCase))
    return suite

