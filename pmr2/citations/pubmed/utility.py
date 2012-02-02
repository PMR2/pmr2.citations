import re
from os.path import dirname, join

from SOAPpy import WSDL
from SOAPpy.Client import SOAPTimeoutError
from SOAPpy.Errors import Error

from pmr2.citations.content import Citation
from pmr2.citations.utility import BaseCitationImporter

_PUBMED_WSDL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/' \
              'efetch_pubmed.wsdl'
PUBMED_WSDL = join(dirname(__file__), 'efetch_pubmed.wsdl')


# very naive way to match the identifiers we support.
pmid_pattern = re.compile('[0-9]*$')

class PubmedCitationImporter(BaseCitationImporter):

    description = u'Pubmed SOAP Importer'

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

    def extractId(self, identifier):
        """\
        Very naive way to extract what looks like an pubmed identifier.
        """

        return pmid_pattern.findall(identifier)[0]

    def parse(self, pmid, *a, **kw):
        """\
        Convert pmid into a citation object.
        """

        def to_medline(article):
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
                author = [author]
            return [u'%s %s' % (a.LastName, a.Initials) for a in author]

        def to_ids(id_):
            # assume info and miriam are all valid
            miriam_base = u'urn:miriam:pubmed:%s'
            info_base = u'info:pmid/%s'
            return [miriam_base % id_, info_base % id_]

        # XXX need to verify that we already have this item.

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
        obj_id = str('pmid-%s' % pmid)
        article = raw.PubmedArticle.MedlineCitation.Article

        citation = Citation(obj_id)
        citation.ids = to_ids(pmid)
        citation.title = unicode(article.ArticleTitle)
        citation.creator = to_author_list(article)
        citation.issued = unicode(article.Journal.JournalIssue.PubDate.Year)
        citation.abstract = unicode(article.Abstract.AbstractText)
        citation.bibliographicCitation = to_medline(article)

        return [citation]

    def parseId(self, pmid):
        # automatically convert miriam base and info base to plain
        # pubmed identifier here?
        return self.parse(pmid)
