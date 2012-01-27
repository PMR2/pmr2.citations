import zope.interface
import zope.component

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from pmr2.citations.interfaces import ICitationImporter


class CitationImporterVocab(SimpleVocabulary):

    def __init__(self, context):
        self.context = context
        values = zope.component.getUtilitiesFor(ICitationImporter)
        terms = [SimpleTerm(i[0], i[0], i[1].description) for i in values]
        super(CitationImporterVocab, self).__init__(terms)

def CitationImporterVocabFactory(context):
    return CitationImporterVocab(context)
zope.interface.alsoProvides(CitationImporterVocabFactory, IVocabularyFactory)
