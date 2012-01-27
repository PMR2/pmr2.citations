import zope.component
import zope.interface

from z3c.form import form, field, button, interfaces

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pmr2.app.browser import form

from pmr2.citations.interfaces import ICitationImporter
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
        method = data.get('import_method')
        identifier = data.get('identifier')
        return self.parseAndAdd(method, identifier)

    def parseAndAdd(self, method, identifier):
        """\
        Use the import method to import citation(s) based on the 
        identifier into the current context.
        """

        utility = zope.component.queryUtility(ICitationImporter, name=method)
        utility.parseIdInto(self.context, identifier)
