import zope.interface
import zope.schema


class ICitationImportForm(zope.interface.Interface):
    """\
    Fields for the citation add form.

    These only include extra fields.
    """

    import_method = zope.schema.Choice(
        title=u'Import method',
        description=u'Select one of the available import methods.',
        vocabulary='pmr2.citations.vocab.import_methods',
        required=True,
    )

    identifier = zope.schema.TextLine(
        title=u'Import identifier',
        description=u'The identifier for the import.  This is specific to the '
                     'selected import method.',
        required=True,
    )
