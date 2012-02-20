import zope.component
import zope.interface

from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry

from pmr2.citations.interfaces import ICitation
from pmr2.citations.interfaces import ICitationSettings
from pmr2.citations.interfaces import ICitationImporter
from pmr2.citations.interfaces import ICitationExporter


class CitationManager(object):
    """\
    The citation manager

    Manages all citations in this Plone instance - returns the object
    within the CMS that matches the requested id, and/or import one if
    it does not already exist if it is possible.
    """

    def __init__(self, context, request):
        # This requires both context and request to allow this to be
        # easily integrated into a form just by extension.
        self.context = context
        self.request = request

    def getCitation(self, identifier):
        """\
        Get citation by identifier.
        """

        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(
            portal_type='Citation', 
            pmr2_citations=identifier,
        )
        return results

    def getDefaultContainer(self):
        registry = zope.component.queryUtility(IRegistry)
        settings = registry.forInterface(ICitationSettings,
            prefix="pmr2.citations.settings", check=False)
        if not settings.default_path:
            raise ValueError('no default path')
        container = self.context.restrictedTraverse(settings.default_path)
        return container

    def importCitationFromId(self, identifier, 
            importer=None, use_context=False):
        """
        Acquire a citation from the identifier, and generate a citation
        then import it to context.

        importer is a specific importer identified by name.  If 
        specified, auto-detection will not be used.

        If use_context is False, acquire the destination container from
        the location defined in registry.
        """

        if use_context:
            container = self.context
        else:
            # this can die here.
            container = self.getDefaultContainer()

        if importer:
            u = zope.component.queryUtility(ICitationImporter, name=importer)
            if not u:
                raise ValueError('importer `%s` not found', importer)
            return u.parseIdInto(container, identifier)

        importers = zope.component.getUtilitiesFor(ICitationImporter)
        extracted = None
        for k, i in importers:
            extracted = i.extractId(identifier)
            if extracted:
                break

        if not extracted:
            return None

        i.parseIdInto(container, identifier)
