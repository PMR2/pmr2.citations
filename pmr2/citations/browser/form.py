import zope.component
import zope.interface

from plone.registry.interfaces import IRegistry

from z3c.form import form, field, button, interfaces

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pmr2.app.browser import form

from pmr2.citations.interfaces import ICitationImporter, ICitationSettings
from pmr2.citations.interfaces import ICitationManager
from pmr2.citations.browser.interfaces import ICitationImportForm


class CitationImportForm(form.PostForm):
    """\
    Citation viewer
    """

    fields = field.Fields(ICitationImportForm)
    ignoreContext = True

    @button.buttonAndHandler(u'Import Citation', name='import')
    def importCitation(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        method = data.get('import_method', None)
        identifier = data.get('identifier')
        to_here = data.get('import_here', False)

        manager = zope.component.queryMultiAdapter(
            (self.context, self.request), ICitationManager)

        try:
            result = manager.importCitationFromId(identifier, method, to_here)
        except:
            # XXX set error message?
            raise
        return

        # use the CitationManager isntead.
        # XXX get list of identifiers added
        # XXX build links to them
        # XXX save import result?


class CitationSettingsForm(form.EditForm):
    """\
    Citation setting form
    """

    fields = field.Fields(ICitationSettings)

    def getContent(self):
        registry = zope.component.queryUtility(IRegistry)
        settings = registry.forInterface(ICitationSettings, 
            prefix="pmr2.citations.settings", check=False)
        return settings
