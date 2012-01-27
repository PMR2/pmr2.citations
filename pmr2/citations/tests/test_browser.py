from cStringIO import StringIO
from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from Zope2.App.zcml import load_config
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.layer import onteardown

from plone.z3cform.interfaces import IWrappedForm

from pmr2.testing.base import TestRequest

from pmr2.citations.interfaces import ICitation
from pmr2.citations.pubmed.utility import PubmedCitationImporter
from pmr2.citations.content import Citation
from pmr2.citations.browser import form


@onsetup
def setup():
    import pmr2.citations
    import pmr2.citations.tests
    fiveconfigure.debug_mode = True
    load_config('configure.zcml', pmr2.citations)
    load_config('test.zcml', pmr2.citations.tests)
    fiveconfigure.debug_mode = False

setup()
ptc.setupPloneSite() #products=('pmr2.citations',))


class CitationBrowserTestCase(ptc.PloneTestCase):
    """\
    Standard test for the pubmed API.
    """

    def test_0000_import_form_render(self):
        context = self.folder
        request = TestRequest()
        f = form.CitationImportForm(context, request)
        # force this instance as a wrapped form to not render cruft.
        zope.interface.directlyProvides(f, IWrappedForm)
        f.update()
        result = f.render()
        self.assertTrue('test_json' in result)

    def test_0100_import_form_import(self):
        context = self.folder
        request = TestRequest()
        f = form.CitationImportForm(context, request)
        f.parseAndAdd('test_json', 'test.cite.1.json')
        self.assertEqual(self.folder.testj1.title, u'Test Citation Title')


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CitationBrowserTestCase))
    return suite

