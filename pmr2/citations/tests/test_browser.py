from cStringIO import StringIO
from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from plone.registry.interfaces import IRegistry

from Zope2.App.zcml import load_config
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.layer import onteardown

from plone.z3cform.interfaces import IWrappedForm

from pmr2.testing.base import TestRequest

from pmr2.citations.interfaces import ICitation, ICitationSettings
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
        context = self.portal
        request = TestRequest()
        f = form.CitationImportForm(context, request)
        # force this instance as a wrapped form to not render cruft.
        zope.interface.directlyProvides(f, IWrappedForm)
        f.update()
        result = f.render()
        self.assertTrue('test_json' in result)

    def test_0100_import_form_all_specified(self):
        context = self.portal
        request = TestRequest(form={
            'form.widgets.import_method': 'test_json',
            'form.widgets.identifier': u'urn:example:json:test.cite.1',
            'form.widgets.import_here': [u'true'],
            'form.buttons.import': 1,
        })
        f = form.CitationImportForm(context, request)
        f.update()
        self.assertEqual(self.portal.testj1.title, u'Test Citation Title')

    def test_0101_import_form_import_default(self):
        context = self.folder
        request = TestRequest(form={
            'form.widgets.import_method': 'test_json',
            'form.widgets.identifier': u'urn:example:json:test.cite.2',
            'form.buttons.import': 1,
        })
        f = form.CitationImportForm(context, request)
        f.update()
        self.assertFalse('testj2' in self.folder)

    def test_0102_import_form_import_default(self):
        registry = zope.component.queryUtility(IRegistry)
        settings = registry.forInterface(ICitationSettings,
            prefix="pmr2.citations.settings", check=False)
        settings.default_path = '/plone/Members/test_user_1_'

        context = self.folder
        request = TestRequest(form={
            'form.widgets.import_method': 'test_json',
            'form.widgets.identifier': u'urn:example:json:test.cite.2',
            'form.buttons.import': 1,
        })
        f = form.CitationImportForm(context, request)
        f.update()
        self.assertEqual(self.folder.testj2.title, u'Number 2 Test')


class CitationBrowserPubmedTestCase(ptc.PloneTestCase):
    """\
    The core citation test case.
    """

    # really don't want this to run unless explicitly specified
    level = 9

    def test_0100_import_form(self):
        registry = zope.component.queryUtility(IRegistry)
        settings = registry.forInterface(ICitationSettings,
            prefix="pmr2.citations.settings", check=False)
        settings.default_path = '/plone/Members/test_user_1_'

        context = self.portal
        request = TestRequest(form={
            'form.widgets.identifier': u'urn:miriam:pubmed:12991237',
            'form.buttons.import': 1,
        })
        f = form.CitationImportForm(context, request)
        f.update()
        self.assertEqual(self.folder['pmid-12991237'].title, 
            u'A quantitative description of membrane current and its '
             'application to conduction and excitation in nerve.')


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CitationBrowserTestCase))
    suite.addTest(makeSuite(CitationBrowserPubmedTestCase))
    return suite

