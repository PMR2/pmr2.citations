from plone.indexer import indexer

from pmr2.citations.interfaces import ICitation


@indexer(ICitation)
def pmr2_citations_id(context):
    return context.ids

@indexer(ICitation)
def pmr2_citations_title(context):
    # Unsearchable
    return context.title

@indexer(ICitation)
def pmr2_citations_creator(context):
    # Only return family names.
    return [i.split()[0] for i in context.creator]

@indexer(ICitation)
def pmr2_citations_issued(context):
    return context.issued
