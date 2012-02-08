import zope.interface
import zope.schema


class ICitationSettings(zope.interface.Interface):

    default_path = zope.schema.ASCIILine(
        title=u'Default citation path',
        description=u'The path on the portal where imported citations are '
                     'placed.',
        required=True,
        default='/',
    )


class ICitation(zope.interface.Interface):
    """\
    General citation annotation.  Losely based on Dublin Core.

    This is similar to the CMF one, but ultimately different due to how
    that one is for metadata for the object that implements this, rather
    than the content which is what we are really tracking.
    """

    id = zope.schema.ASCIILine(
        title=u'Object identifier',
        description=u'ID for this object; included here in interface for'
                     'completeness',
        required=True,
    )

    ids = zope.schema.List(
        title=u'Citation Identifiers',
        description=u'A list of URNs that can represent this resource.',
        value_type=zope.schema.TextLine(title=u'ID'),
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
        value_type=zope.schema.TextLine(title=u'Author'),
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

    description = zope.schema.TextLine(
        title=u'Description',
        required=False,
    )

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

    description = zope.schema.TextLine(
        title=u'Description',
        required=False,
    )

    id_patterns = zope.schema.List(
        title=u'Identifier Patterns',
        description=u'The patterns valid as a source for this importer.',
        required=False,
        default=None,
        value_type=zope.schema.TextLine(title=u'Values',),
    )

    # perhaps a method to compile expressions and return results later?

    def addInto(context, items):
        """
        Add citations into the context.

        Items should be a list of objects implemented the ICitation
        interface.
        """

    def extractId(identifier):
        """\
        Extract Id from input identifier.
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

    def parseId(identifier):
        """\
        Get a list of citations based on a identifier string.
        """

    def parseIdInto(context, identifier, *a, **kw):
        """\
        Combines the above two functions.
        """
