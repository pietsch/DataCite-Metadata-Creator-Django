# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class publisher_model(models.Model):
    """Publisher model."""
    name = models.CharField(u'Name', max_length=1000)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name = u'Publisher'
        verbose_name_plural = u'Publishers'
    def __unicode__(self):
        return self.name

# class author_model(models.Model):
#     name = models.CharField(max_length=1000, blank=True)
#     class Meta:
#         verbose_name = u'Author'
#     def __unicode__(self):
#         return "%s" % (self.name, )

# class authors_model(models.Model):
#     author = models.ForeignKey("author_model")
#     class Meta:
#         verbose_name = u'Authors'
#     def __unicode__(self):
#         return "id: %s" % (self.id, )


class resource_model(models.Model):
    """Resource model."""

    title = models.CharField(u'Title', max_length=1000)  ## TODO multiple titles allowed!

    subtitle = models.CharField(u'Subtitle', max_length=1000, blank=True)

#     titles = models.ManyToManyField("title_model",
#         help_text=u'''A name or title by which a resource is known.''')
# 
# class title_model(models.Model):
#     TITLE_TYPES = (
#         (u'AlternativeTitle', u'Alternative title'),
#         (u'Subtitle', u'Subtitle'),
#         (u'TranslatedTitle', u'Translated title'),
#     )
#     titleType = models.CharField(u'Type', max_length=20, choices=TITLE_TYPES, blank=True)
#     title = models.CharField(max_length=1000)
#     class Meta:
#         verbose_name = u'Title'
#     def __unicode__(self):
#         return self.title

    slug = models.SlugField(u'Unique name (slug)', unique=True)

    doi = models.CharField(max_length=128, editable=False)

    creators = models.ManyToManyField("creator_model",
        help_text=u'''Format: Family, Given.<br/>
Meaning: The main researchers involved working on the data, or the authors of the publication in priority order. May be a corporate/institutional or personal name.''')

    publisher = models.ForeignKey(publisher_model, help_text=u'''Examples: “World Data Center for Climate (WDCC)”; “GeoForschungsZentrum Potsdam (GFZ)”; “Geological Institute, University of Tokyo”<br/>
Meaning: A holder of the data (including archives as appropriate) or institution which submitted the work. Any others may be listed as contributors. This property will be used to formulate the citation, so consider the prominence of the role.<br/>
Note: In the case of datasets, "publish" is understood to mean making the data available to the community of researchers.''')
    
    publicationYear = models.IntegerField(u'Year of publication',
        help_text=u'Format: “YYYY”. Meaning: Year when the data is made publicly available. If an embargo period has been in effect, use the date when the embargo period ends.')

    subjects = models.ManyToManyField("subject_model", blank=True,
        help_text=u'Subject, keywords, classification codes, or key phrases describing the resource.')

    contributors = models.ManyToManyField("contributor_model", blank=True,
        help_text=u'''The institution or person responsible for collecting, creating, or otherwise contributing to the developement of the dataset.<br/>
The personal name format should be: Family, Given.''')

    descriptions = models.ManyToManyField("description_model", blank=True,
        help_text=u'An informal description.')

    dates = models.ManyToManyField("date_model", blank=True,  ## TODO date ranges sometimes allowed!!!
        help_text=u'''Different dates relevant to the work.<br />
Format: YYYY or YYYY-MM-DD or any other format described in W3CDTF (http://www.w3.org/TR/NOTE-datetime)''')

    language = models.CharField(max_length=3, blank=True,
        help_text=u'''Primary language of the resource. Allowed values from: ISO 639-2/B, ISO 639-3''')

    resourceType = models.ForeignKey("resourceType_model", verbose_name="Resource type", blank=True, null=True,
        help_text=u'''The type of a resource. You may enter an additional free text description.<br />
Use the resourceTypeGeneral attribute to choose the general type of the resource from the controlled list.''')

    alternateIdentifiers = models.ManyToManyField("alternateIdentifiers_model", verbose_name="Alternate IDs", blank=True,
        help_text=u'''An identifier other than the primary identifier applied to the resource being registered.<br />
This may be any alphanumeric string which is unique within its domain of issue. The format is open.''')

    relatedIdentifiers = models.ManyToManyField("relatedIdentifier_model", verbose_name="Related IDs", blank=True,
        help_text=u'''Identifiers of related resources. Use this property to indicate subsets of properties, as appropriate.''')

    sizes = models.ManyToManyField("size_model", blank=True,
        help_text=u'''Unstructured size information about the resource.''')

    formats = models.ManyToManyField("format_model", blank=True,
        help_text=u'''Technical format of the resource.<br />
Use file extension or MIME type where possible.''')

    version = models.CharField(max_length=1000, blank=True,
        help_text=u'''Version number of the resource. If the primary resource has changed the version number increases.<br />
Register a new DOI (or primary identifier) when the version of the resource changes to enable the citation of the exact version of a research dataset (or other resource). May be used in conjunction with properties 11 and 12 (AlternateIdentifier and RelatedIdentifier) to indicate various information updates.''')

    rights = models.CharField(max_length=1000, blank=True)

    submitter = models.ForeignKey(User, null=True, blank=True, editable=False)

    date_created = models.DateTimeField(editable=False)

    date_updated = models.DateTimeField(editable=False)

    class Meta:
        verbose_name = u'Resource'
        verbose_name_plural = u'Resources: Enter new datasets here'
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(resource_model, self).save(*args, **kwargs)

class creator_model(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    class Meta:
        verbose_name = u'Creator'
    def __unicode__(self):
        return self.name

class subject_model(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    class Meta:
        verbose_name = u'Subject'
    def __unicode__(self):
        return self.name

class contributor_model(models.Model):
    CONTRIBUTOR_TYPES = (
        (u'ContactPerson', u'contact person'),
        (u'DataCollector', u'data collector'),
        (u'DataManager', u'data manager'),
        (u'Distributor', u'distributor'),
        (u'Editor', u'editor'),
        (u'Funder', u'funder'),
        (u'HostingInstitution', u'hosting institution'),
        (u'Producer', u'producer'),
        (u'ProjectLeader', u'project leader'),
        (u'ProjectMember', u'project member'),
        (u'RegistrationAgency', u'registration agency'),
        (u'RegistrationAuthority', u'registration authority'),
        (u'RelatedPerson', u'related person'),
        (u'RightsHolder', u'rights holder'),
        (u'Researcher', u'researcher'),
        (u'Sponsor', u'sponsor'),
        (u'Supervisor', u'supervisor'),
        (u'WorkPackageLeader', u'work package leader'),
    )
    contributorType = models.CharField(u'Type', max_length=30, choices=CONTRIBUTOR_TYPES)
    name = models.CharField(max_length=1000)
    class Meta:
        verbose_name = u'Contributor'
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.contributorType)

class date_model(models.Model):
    DATE_TYPES = (
        (u'Accepted', u'Accepted: The date that the publisher accepted the resource into their system.'),
        (u'Available', u'Available: The date the resource is made publicly available. May be a range.'),
        (u'Copyrighted', u'Copyrighted: The specific, documented date at which the resource receives a copyrighted status, if applicable.'),
        (u'Created', u'Created: The date the resource itself was put together; this could be a date range or a single date for a final component, e.g., the finalised file with all of the data.'),
        (u'EndDate', u'EndDate: Use if any other date type covers a range'),
        (u'Issued', u'Issued: The date that the resource is published or distributed e.g. to a data center.'),
        (u'StartDate', u'StartDate: Use if any other date type covers a range.'),
        (u'Submitted', u'Submitted: The date the creator submits the resource to the publisher. This could be different from Accepted if the publisher then applies a selection process.'),
        (u'Updated', u'Updated: The date of the last update to the resource, when the resource is being added to. May be a range.'),
        (u'Valid', u'Valid: The date or date range during which the dataset or resources are accurate. May be a range.'),
    )
    dateType = models.CharField(max_length=15, choices=DATE_TYPES)
    date = models.DateField()
    class Meta:
        verbose_name = u'Date'
    def __unicode__(self):
        return "%s" % (self.date, )


class alternateIdentifiers_model(models.Model):
    alternateIdentifierType = models.CharField(u'Type', max_length=1000)
    alternateIdentifier = models.CharField(u'ID', max_length=1000)
    class Meta:
        verbose_name = u'Alternate identifier'
    def __unicode__(self):
        return "%s (%s)" % (self.alternateIdentifier, self.alternateIdentifierType)

class resourceType_model(models.Model):
    RESOURCE_TYPES = (
        (u'Collection', u'Collection'),
        (u'Dataset', u'Dataset'),
        (u'Event', u'Event'),
        (u'Film', u'Film'),
        (u'Image', u'Image'),
        (u'InteractiveResource', u'Interactive resource'),
        (u'Model', u'Model'),
        (u'PhysicalObject', u'Physical object'),
        (u'Service', u'Service'),
        (u'Software', u'Software'),
        (u'Sound', u'Sound'),
        (u'Text', u'Text'),
    )
    resourceTypeGeneral = models.CharField(max_length=30, choices=RESOURCE_TYPES)
    description = models.CharField(max_length=1000, blank=True)
    class Meta:
        verbose_name = u'Resource type'
    def __unicode__(self):
        return "%s (%s)" % (self.resourceTypeGeneral, self.description)

class relatedIdentifier_model(models.Model):
    IDENTIFIER_TYPES = (
        (u'ARK', u'ARK'),
        (u'DOI', u'DOI'),
        (u'EAN13', u'EAN13'),
        (u'EISSN', u'EISSN'),
        (u'Handle', u'Handle'),
        (u'ISBN', u'ISBN'),
        (u'ISSN', u'ISSN'),
        (u'ISTC', u'ISTC'),
        (u'LISSN', u'LISSN'),
        (u'LSID', u'LSID'),
        (u'PURL', u'PURL'),
        (u'UPC', u'UPC'),
        (u'URL', u'URL'),
        (u'URN', u'URN'),
    )
    RELATION_TYPES = (
        (u'IsCitedBy', u'IsCitedBy: indicates that B includes A in a citation'),
        (u'Cites', u'Cites: indicates that A includes B in a citation'),
        (u'IsSupplementTo', u'IsSupplementTo: indicates that A is a supplement to B'),
        (u'IsSupplementedBy', u'IsSupplementedBy: indicates that B is a supplement to A'),
        (u'IsContinuedBy', u'IsContinuedBy: indicates A is continued by the work B'),
        (u'Continues', u'Continues: indicates A is a continuation of the work B'),
        (u'IsNewVersionOf', u'IsNewVersionOf: indicates B is a new edition of A, where the new edition has been modified or updated'),
        (u'IsPreviousVersionOf', u'IsPreviousVersionOf: indicates B is a previous edition of A'),
        (u'IsPartOf', u'IsPartOf: indicates A is a portion of B'),
        (u'HasPart', u'HasPart: indicates A includes the part B'),
        (u'IsReferencedBy', u'IsReferencedBy: indicates A is used as a source of information by B'),
        (u'References', u'References: indicates B is used as a source of information for A'),
        (u'IsDocumentedBy', u'IsDocumentedBy: indicates B is documentation about/explaining A'),
        (u'Documents', u'Documents: indicates A is documentation about/explaining B'),
        (u'IsCompiledBy', u'IsCompiledBy: indicates B is used to compile or create A'),
        (u'Compiles', u'Compiles: indicates B is the result of a compile or creation event using A'),
        (u'IsVariantFormOf', u'IsVariantFormOf: indicates B is a variant or different form of A, e.g. calculated or calibrated form or different packaging'),
        (u'IsOriginalFormOf', u'IsOriginalFormOf: indicates B is the original form of A'),
    )
    relatedIdentifier = models.CharField(u'ID', max_length=1000)
    relatedIdentifierType = models.CharField(u'ID type', max_length=10, choices=IDENTIFIER_TYPES)
    relationType = models.CharField(u'Relation', max_length=30, choices=RELATION_TYPES)
    class Meta:
        verbose_name = u'Relation type'
    def __unicode__(self):
        return "%s %s (%s)" % (self.relationType, self.relatedIdentifier, self.relatedIdentifierType)

class size_model(models.Model):
    size = models.CharField(max_length=100)
    class Meta:
        verbose_name = u'Size'
    def __unicode__(self):
        return self.size

class format_model(models.Model):
    name = models.CharField(max_length=1000)
    class Meta:
        verbose_name = u'Subject'
    def __unicode__(self):
        return self.name

class description_model(models.Model):
    DESCRIPTION_TYPES = (
        (u'Abstract', u'Abstract'),
        (u'SeriesInformation', u'Series information'),
        (u'TableOfContents', 'Table of contents'),
        (u'Other', 'Other')
    )
    descriptionType = models.CharField(u'Type', max_length=20, choices=DESCRIPTION_TYPES)
    description = models.TextField(u'Beschreibung', blank=True)
    class Meta:
        verbose_name = u'Description type'
    def __unicode__(self):
        return "%s: %s" % (self.descriptionType, self.description)
