from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CitationView(BrowserView):
    """\
    Citation viewer
    """

    template = ViewPageTemplateFile('citation_view.pt')

    def creator(self):
        return ', '.join(self.context.creator)
    
    def title(self):
        return self.context.title

    def bibliographicCitation(self):
        return self.context.bibliographicCitation
    
    def abstract(self):
        return self.context.abstract

    def references(self):
        # XXX this is still based off the cmeta ids for now.
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(
                cmeta_citation_id=self.context.ids,
                pmr2_review_state='published',
            )
        for i in results:
            yield {
                'href': i.getURL(),
                'title': i.Title,
                'description': i.Description,
            }

    def __call__(self):
        return self.template()
