from cStringIO import StringIO
from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from plone.registry.interfaces import IRegistry

from Products.PloneTestCase import PloneTestCase as ptc

from pmr2.citations.interfaces import ICitation, ICitationSettings
from pmr2.citations.utility import *
from pmr2.citations.adapter import CitationManager
from pmr2.citations.content import Citation

#from pmr2.citations.tests.base import TestCitation


ptc.setupPloneSite(products=('pmr2.citations',))


class CitationTestCase(ptc.PloneTestCase):
    """\
    The core citation test case.
    """

    def afterSetUp(self):
        self.container = {}
        self.exporter = JsonCitationExporter()
        self.importer = JsonCitationImporter()

    def test_0000_json_import_export_cycle(self):
        testid = 'test1'
        citation = Citation(testid)
        citation.ids = [u'urn:test1',]
        citation.title = u'Test Title One'
        citation.creator = [u'Tester One', u'Tester Two']
        citation.issued = u'2001-01-01'
        citation.bibliographicCitation = u'Test Journal'
        citation.abstract = None

        self.container[citation.id] = citation
        jsonstr = self.exporter.export(self.container)
        jsonstream = StringIO(jsonstr)

        new_container = self.folder
        self.importer.parseInto(new_container, jsonstream)
        
        self.assertEqual(new_container[testid].id, 
                         self.container[testid].id)
        self.assertEqual(new_container[testid].ids[0], 
                         self.container[testid].ids[0])
        self.assertEqual(new_container[testid].title, 
                         self.container[testid].title)
        self.assertEqual(new_container[testid].creator, 
                         self.container[testid].creator)


class CitationManagerTestCase(ptc.PloneTestCase):
    """\
    The core citation test case.
    """

    def afterSetUp(self):
        self.container = {}
        self.manager = CitationManager(self.portal, None)

    def test_0000_general_test(self):
        id1 = u'urn:non_working_example:1'
        self.assertEqual(len(self.manager.getCitation(id1)), 0)

    def test_1000_import_test_registry_fail(self):
        testid = u'urn:example:json:test.cite.1'
        self.assertRaises(ValueError,
            self.manager.importCitationFromId, testid)

    def test_1010_import_test_registry(self):
        registry = zope.component.queryUtility(IRegistry)
        settings = registry.forInterface(ICitationSettings,
            prefix="pmr2.citations.settings", check=False)
        settings.default_path = '/plone'
        testid = u'urn:example:json:test.cite.1'
        self.manager.importCitationFromId(testid)
        self.assertTrue('testj1' in self.portal)


class CitationManagerWithPubmedTestCase(ptc.PloneTestCase):
    """\
    The core citation test case.
    """

    # really don't want this to run unless explicitly specified
    level = 9

    def afterSetUp(self):
        self.container = {}
        self.manager = CitationManager(self.portal, None)

    def test_1010_import_test_registry(self):
        registry = zope.component.queryUtility(IRegistry)
        settings = registry.forInterface(ICitationSettings,
            prefix="pmr2.citations.settings", check=False)
        settings.default_path = '/plone'
        testid = u'urn:miriam:pubmed:17432928'
        self.manager.importCitationFromId(testid)
        self.assertTrue('pmid-17432928' in self.portal)


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CitationTestCase))
    suite.addTest(makeSuite(CitationManagerTestCase))
    return suite

