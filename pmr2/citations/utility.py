import re
import json

import zope.interface
import zope.component
import zope.event
import zope.lifecycleevent
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry

from pmr2.citations.interfaces import ICitation
from pmr2.citations.interfaces import ICitationSettings
from pmr2.citations.interfaces import ICitationImporter
from pmr2.citations.interfaces import ICitationExporter

from pmr2.citations.content import Citation


class BaseCitationImporter(object):
    """\
    The basic citation importer.

    This will create and return a citation atct object from input, which
    is a stream of json.
    """

    zope.interface.implements(ICitationImporter)

    description = u''
    id_patterns = None

    def __init__(self):
        pass

    def addInto(self, context, items):
        """\
        Add the items to the context.
        """

        for item in items:
            zope.event.notify(zope.lifecycleevent.ObjectCreatedEvent(item))
            context[item.id] = item

    def extractId(self, identifier):
        if not self.id_patterns:
            return None
        for i in self.id_patterns:
            p = re.compile(i)
            result = p.findall(identifier)
            if result:
                # Only return the first result.
                return result[0]
        return None

    def parse(self, *a, **kw):
        raise NotImplementedError

    def parseInto(self, context, *a, **kw):
        citations = self.parse(*a, **kw)
        self.addInto(context, citations)

    def parseId(self, identifier):
        raise NotImplementedError

    def parseIdInto(self, context, identifier):
        citations = self.parseId(identifier)
        self.addInto(context, citations)


class JsonCitationImporter(BaseCitationImporter):
    """\
    Imports from a json export.
    """

    description = u'Citation JSON Importer'

    def parse(self, stream=None, *a, **kw):

        if not hasattr(stream, 'read'):
            raise TypeError('input must be a stream')

        raw_items = json.load(stream)
        results = []

        for raw_citation in raw_items:
            rawid = raw_citation['id']
            item = Citation(str(rawid))
            item.ids = raw_citation['ids']
            item.title = raw_citation['title']
            item.creator = raw_citation['creator']
            item.issued = raw_citation['issued']
            item.bibliographicCitation = raw_citation['bibliographicCitation']
            results.append(item)

        return results

    def parseId(self, identifier):
        """
        Idenitifier in this case will be a path, but we don't implement
        this yet.
        """

        raise NotImplementedError

        # we can have this, but need to figure out how to handle this
        # in a secure way.
        stream = open(identifier)
        return self.parse(stream)


class JsonCitationExporter(object):
    """\
    Returns all citation objects in container as a JSON string.
    """

    zope.interface.implements(ICitationExporter)

    description = u'Citation JSON Exporter'

    def find_citations(self, container):
        """\
        Find all citation objects within container.
        """

        # XXX when the raw values are indexed correctly, portal_catalog
        # might be a better way, for now we skip this.
        # 
        # try:
        #     catalog = getToolByName(container, 'portal_catalog')
        # except AttributeError:
        #     return [i for i in container.values() if ICitation.providedBy(i)]
        # 
        # brains = catalog(portal_type='Citation')
        # # perhaps use a generator?
        # return [i.getObject() for i in self._catalog(brains)]

        # and just do this...
        return [i for i in container.values() if ICitation.providedBy(i)]

    def _export(self, citation):
        names = ICitation.names()
        result = {}
        for k in names:
            result[k] = getattr(citation, k, None)
        return result

    def export(self, container):
        citations = self.find_citations(container)
        results = []
        for citation in citations:
            raw = self._export(citation)
            results.append(raw)
        return json.dumps(results)
