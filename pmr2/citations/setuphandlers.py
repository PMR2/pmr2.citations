import zope.component
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from pmr2.citations.interfaces import ICitationSettings


def register_settings(context):
    """\
    Register the settings interface into plone registry.
    """

    registry = zope.component.getUtility(IRegistry)
    registry.registerInterface(ICitationSettings, 
        prefix="pmr2.citations.settings")

def importVarious(context):
    """Install the ProtocolAuthPAS plugin"""

    register_settings(context)

