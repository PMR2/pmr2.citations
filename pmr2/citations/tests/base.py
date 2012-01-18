import zope.interface
import zope.component

from pmr2.citations.interfaces import ICitation


class TestCitation(object):
    """\
    Test citaiton object.
    """

    zope.interface.implements(ICitation)

    def __init__(self, id_):
        self.id = id_

