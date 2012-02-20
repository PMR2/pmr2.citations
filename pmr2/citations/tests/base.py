from os.path import dirname, join

import zope.interface
import zope.component

from pmr2.citations.interfaces import ICitation
from pmr2.citations.utility import JsonCitationImporter

input_file = lambda p: join(dirname(__file__), 'input', p + '.json')


class TestCitation(object):
    """\
    Test citaiton object.
    """

    zope.interface.implements(ICitation)

    def __init__(self, id_):
        self.id = id_


class TestJsonCitationImporter(JsonCitationImporter):

    description = u'Test JSON Importer'
    id_patterns = [
        u'^urn:example:json:(.*)$',
    ]

    def parseId(self, identifier):
        """\
        Identifier will be file names in the test input directory.
        """

        filename = self.extractId(identifier)
        fp = open(input_file(filename))
        try:
            results = self.parse(fp)
        finally:
            fp.close()
        return results
