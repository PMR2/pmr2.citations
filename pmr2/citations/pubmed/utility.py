from SOAPpy import WSDL
from SOAPpy.Client import SOAPTimeoutError
from SOAPpy.Errors import Error

from pmr2.citations.content import Citation
from pmr2.citations.utility import BaseCitationImporter

PUBMED_WSDL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/' \
              'efetch_pubmed.wsdl'

class PubmedCitationImporter(BaseCitationImporter):

    def __init__(self):
        self._init_importer()

    def _init_importer(self, db=None, service_url=None):
        if db is None:
            db = 'pubmed'
        if service_url is None:
            self.service_url = PUBMED_WSDL
        self.db = 'pubmed'

    @property
    def service(self):
        if not hasattr(self, '_service'):
            self._service = WSDL.Proxy(self.service_url)
        return self._service

    def parse(self, pmid, *a, **kw):
        """\
        Convert pmid into a citation object.
        """

        def to_medline(article):
            # 1977 Jun;268(1):177-210
            abbr = article.Journal.ISOAbbreviation
            pubdate = u' '.join(list(article.Journal.JournalIssue.PubDate))
            volume = article.Journal.JournalIssue.Volume
            issue = article.Journal.JournalIssue.Issue
            pages = article.Pagination.MedlinePgn
            result = u'%s %s;%s(%s):%s.' % (abbr, pubdate, volume, issue, pages)
            return result

        def to_author_list(article):
            author = article.AuthorList.Author
            if not isinstance(author, list):
                author = list(author)
            return [u'%s %s' % (a.LastName, a.Initials) for a in author]

        try:
            raw = self.service.run_eFetch(db=self.db, id=pmid)
        except SOAPTimeoutError:
            # XXX handle timeout
            raise
        except Error:
            # XXX any SOAP error
            raise
        except:
            # Other errors will just be raised.
            raise

        # using info for now
        citation_id = 'info:pmid/%s' % pmid
        article = raw.PubmedArticle.MedlineCitation.Article

        citation = Citation(citation_id)
        citation.title = unicode(article.ArticleTitle)
        citation.creator = to_author_list(article)
        citation.issued = unicode(article.Journal.JournalIssue.PubDate.Year)
        citation.bibliographicCitation = to_medline(article)

        return [citation]
