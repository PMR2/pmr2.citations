from cStringIO import StringIO
from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from Products.PloneTestCase import PloneTestCase as ptc

from pmr2.citations.interfaces import ICitation
from pmr2.citations.pubmed.utility import PubmedCitationImporter
from pmr2.citations.content import Citation

#from pmr2.citations.tests.base import TestCitation


ptc.setupPloneSite() #products=('pmr2.citations',))


class PubmedCitationTestCase(ptc.PloneTestCase):
    """\
    Live test for the pubmed API.
    """

    def afterSetUp(self):
        self.container = {}
        self.importer = PubmedCitationImporter()

    def test_0000_pubmed_base_test(self):
        testid = '874889'
        objid = 'pmid-874889'

        container = self.folder
        self.importer.parseInto(container, testid)
        
        self.assertEqual(container[objid].id, objid)
        self.assert_('urn:miriam:pubmed:874889' in container[objid].ids)
        self.assert_('info:pmid/874889' in container[objid].ids)
        self.assertEqual(container[objid].title,
           u'Reconstruction of the action potential of ventricular myocardial '
            'fibres.')


def test_suite():
    suite = TestSuite()
    # Uncomment to enable live testing.
    # suite.addTest(makeSuite(PubmedCitationTestCase))
    return suite

