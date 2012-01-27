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

    def __call__(self):
        return self.template()
