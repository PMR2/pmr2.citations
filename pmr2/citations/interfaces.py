import zope.interface
import zope.schema


class ICitation(zope.interface.Interface):
    """\
    General citation annotation.  Losely based on Dublin Core.

    This is similar to the CMF one, but ultimately different due to how
    that one is for metadata for the object that implements this, rather
    than the content which is what we are really tracking.
    """

    id = zope.schema.ASCIILine(
        title=u'Citation Identifier',
        description=u'URN to this citation.',
        required=True,
    )

    title = zope.schema.TextLine(
        title=u'Title',
        description=u'Title of this citation.',
        required=False,
    )

    creator = zope.schema.List(
        title=u'Authors',
        description=u'Authors of this piece of work',
        required=False,
    )

    issued = zope.schema.TextLine(
        title=u'Issued date',
        description=u'Datetime formatted as W3CDTF',
        required=False,
    )

    bibliographicCitation = zope.schema.TextLine(
        title=u'Citation Source',
        description=u'The source of this citation',
        required=False,
    )

    abstract = zope.schema.Text(
        title=u'Abstract',
        required=False,
    )


class ICitationExporter(zope.interface.Interface):
    """
    Interface for the citation exporter.

    Should be implemented as a utility.
    """

    def export(container):
        """
        Export this citation out into some common format for archiving/
        caching.
        """


class ICitationImporter(zope.interface.Interface):
    """\
    Generic citation importer.

    Provides a method that contructs a citation object.
    """

    def addInto(context, items):
        """
        Add citations into the context.

        Items should be a list of objects implemented the ICitation
        interface.
        """

    def parse(*a, **kw):
        """\
        Parse something based on the parameters.

        This is implementation specific.  Should return a list of 
        objects that implements ICitation.
        """

    def parseInto(context, *a, **kw):
        """\
        Combines the above two functions.
        """
