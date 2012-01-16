import zope.interface
import zope.component
from zope.schema import fieldproperty

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.CMFCore.permissions import View

from pmr2.citations.interfaces import ICitation


class Citation(atapi.BaseContent):
    """\
    Core citation object based on the AT base content type.
    """

    zope.interface.implements(ICitation)
    security = ClassSecurityInfo()

    id = fieldproperty.FieldProperty(ICitation['id'])
    title = fieldproperty.FieldProperty(ICitation['title'])
    creator = fieldproperty.FieldProperty(ICitation['creator'])
    issued = fieldproperty.FieldProperty(ICitation['issued'])
    bibliographicCitation = fieldproperty.FieldProperty(
        ICitation['bibliographicCitation'])
    abstract = fieldproperty.FieldProperty(ICitation['abstract'])

atapi.registerType(Citation, 'pmr2.citation')
