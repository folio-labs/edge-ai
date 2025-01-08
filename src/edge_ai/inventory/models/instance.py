from enum import Enum
from typing import List, Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Field, StringConstraints, UUID4

from edge_ai.base.models import (
    Metadata
)

from edge_ai.inventory.models.common import (
    ElectronicAccess,
    Note,
    Tags,
)

class AlternativeTitle(BaseModel):
    alternativeTitleTypeId: UUID4 = Field(None, description='UUID for an alternative title qualifier')
    alternativeTitle: Optional[str] = Field(
        None, description='An alternative title for the resource'
    )
    authorityId: Optional[UUID4] = Field(
        None, description='UUID of authority record that controls an alternative title'
    )


class ClassificationType(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., description='label for the classification type')
    source: Optional[str] = Field(
        None,
        description="label indicating where the classification type entry originates from, i.e. 'folio' or 'local'",
    )
    metadata: Optional[Metadata] = Field(
        None,
        description='Metadata about creation and changes to records, provided by the server (client should not provide)',
        title='Metadata Schema',
    )


class Classification(BaseModel):
    classificationNumber: str = Field(
        ...,
        description='Classification (e.g. classification scheme, classification schedule)',
    )
    classificationTypeId: UUID4 = Field(
        ...,
        description='UUID of classification schema (e.g. LC, Canadian Classification, NLM, National Agricultural Library, UDC, and Dewey)',
    )
    classificationType: Optional[ClassificationType] = Field(
        None, description='Dereferenced classification schema'
    )


class ContributorNameType(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., description='label for the type of contributor name')
    ordering: Optional[str] = Field(
        None,
        description='used for ordering of contributor name types in displays, i.e. in select lists',
    )
    source: Optional[str] = Field(
        None,
        description="origin of the contributor name type record, e.g. 'local', 'consortium' etc.",
    )
    metadata: Optional[Metadata] = Field(
        None,
        description='Metadata about creation and changes to records, provided by the server (client should not provide)',
        title='Metadata Schema',
    )


class Contributor(BaseModel):
    name: str = Field(..., description='Personal name, corporate name, meeting name')
    contributorTypeId: Optional[UUID4] = Field(
        None,
        description='UUID for the contributor type term defined in controlled vocabulary',
    )
    contributorTypeText: Optional[str] = Field(
        None,
        description='Free text element for adding contributor type terms other that defined by the MARC code list for relators',
    )
    contributorNameTypeId: UUID4 = Field(
        ...,
        description='UUID of contributor name type term defined by the MARC code list for relators',
    )
    authorityId: Optional[UUID4] = Field(
        None, description='UUID of authority record that controls the contributor'
    )
    contributorNameType: Optional[ContributorNameType] = Field(
        None, description='Dereferenced contributor-name type'
    )
    primary: Optional[bool] = Field(
        None, description='Whether this is the primary contributor'
    )


class Dates(BaseModel):
    dateTypeId: Optional[UUID4] = Field(None, description='Date type ID')
    date1: Optional[
        Annotated[str, StringConstraints(max_length=4)]
    ] = Field(None, description='Date 1')
    date2: Optional[ 
        Annotated[str, StringConstraints(max_length=4)]
    ] = Field(None, description='Date 2')


class IdentifierTypeObject(BaseModel):
    id: Optional[UUID4] = Field(None, description='unique ID of the ILL policy; UUID')
    name: str = Field(..., description='name of the policy')
    source: str = Field(
        ...,
        description="label indicating where the ILL policy entry originates from, i.e. 'folio' or 'local'",
    )
    metadata: Optional[Metadata] = Field(
        None,
        description='Metadata about creation and changes to records, provided by the server (client should not provide)',
        title='Metadata Schema',
    )


class Identifier(BaseModel):

    value: str = Field(..., description='Resource identifier value')
    identifierTypeId: UUID4 = Field(
        ...,
        description='UUID of resource identifier type (e.g. ISBN, ISSN, LCCN, CODEN, Locally defined identifiers)',
    )
    identifierTypeObject: Optional[IdentifierTypeObject] = Field(
        None,
        description='Information about identifier type, looked up from identifierTypeId',
    )


class InstanceFormat(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., description='label for the Instance format')
    code: str = Field(..., description='distinct code for the Instance format')
    source: str = Field(..., description='origin of the Instance format record')
    metadata: Optional[Metadata] = Field(
        None,
        description='Metadata about creation and changes to records, provided by the server (client should not provide)',
        title='Metadata Schema',
    )


class NatureOfContentTermId(BaseModel):
    __root__: UUID4 = Field(..., description='Single UUID for the Instance nature of content')


class PublicationItem(BaseModel):
    publisher: Optional[str] = Field(
        None, description='Name of publisher, distributor, etc.'
    )
    place: Optional[str] = Field(
        None, description='Place of publication, distribution, etc.'
    )
    dateOfPublication: Optional[str] = Field(
        None, description='Date (year YYYY) of publication, distribution, etc.'
    )
    role: Optional[str] = Field(
        None, description='The role of the publisher, distributor, etc.'
    )


class Series(BaseModel):
    value: str = Field(..., description='Series title value')
    authorityId: Optional[UUID4] = Field(
        None, description='UUID of authority record that controls an series title'
    )

class SourceRecordFormat(Enum):
    MARC_JSON = 'MARC-JSON'


class Subject(BaseModel):
    value: str = Field(..., description='Subject heading value')
    authorityId: Optional[UUID4] = Field(
        None, description='UUID of authority record that controls a subject heading'
    )
    sourceId: Optional[UUID4] = Field(None, description='UUID of subject source')
    typeId: Optional[UUID4] = Field(None, description='UUID of subject type')


class Instance(BaseModel):
    id: UUID4 = Field(None, description='The unique ID of the instance record; a UUID')
    field_version: Optional[int] = Field(
        None, alias='_version', description='Record version for optimistic locking'
    )
    hrid: Optional[str] = Field(
        None,
        description='The human readable ID, also called eye readable ID. A system-assigned sequential ID which maps to the Instance ID',
    )
    matchKey: Optional[str] = Field(
        None,
        description='A unique instance identifier matching a client-side bibliographic record identification scheme, in particular for a scenario where multiple separate catalogs with no shared record identifiers contribute to the same Instance in Inventory. A match key is typically generated from select, normalized pieces of metadata in bibliographic records',
    )
    source: str = Field(
        ...,
        description="The metadata source and its format of the underlying record to the instance record. (e.g. FOLIO if it's a record created in Inventory; MARC if it's a MARC record created in MARCcat or EPKB if it's a record coming from eHoldings; CONSORTIUM-MARC or CONSORTIUM-FOLIO for sharing Instances).",
    )
    title: str = Field(
        ..., description='The primary title (or label) associated with the resource'
    )
    indexTitle: Optional[str] = Field(
        None,
        description='Title normalized for browsing and searching; based on the title with articles removed',
    )
    alternativeTitles: Optional[List[AlternativeTitle]] = Field(
        None,
        description='List of alternative titles for the resource (e.g. original language version title of a movie)',
        unique_items=True,
    )
    editions: Optional[List[str]] = Field(
        None,
        description='The edition statement, imprint and other publication source information',
        unique_items=True,
    )
    series: Optional[List[Series]] = Field(
        None,
        description='List of series titles associated with the resource (e.g. Harry Potter)',
        unique_items=True,
    )
    identifiers: Optional[List[Identifier]] = Field(
        None,
        description='An extensible set of name-value pairs of identifiers associated with the resource',
        min_items=0,
    )
    contributors: Optional[List[Contributor]] = Field(
        None, description='List of contributors', min_items=0
    )
    subjects: Optional[List[Subject]] = Field(
        None, description='List of subject headings', unique_items=True
    )
    classifications: Optional[List[Classification]] = Field(
        None, description='List of classifications', min_items=0
    )
    publication: Optional[List[PublicationItem]] = Field(
        None, description='List of publication items'
    )
    publicationFrequency: Optional[List[str]] = Field(
        None,
        description='List of intervals at which a serial appears (e.g. daily, weekly, monthly, quarterly, etc.)',
        unique_items=True,
    )
    publicationRange: Optional[List[str]] = Field(
        None,
        description='The range of sequential designation/chronology of publication, or date range',
        unique_items=True,
    )
    electronicAccess: Optional[List[ElectronicAccess]] = Field(
        None, description='List of electronic access items'
    )
    dates: Optional[Dates] = Field(None, description='Instance Dates')
    instanceTypeId: UUID4 = Field(
        ...,
        description="UUID of the unique term for the resource type whether it's from the RDA content term list of locally defined",
    )
    instanceFormatIds: Optional[
        List[UUID4]
    ] = Field(
        None,
        description="UUIDs for the unique terms for the format whether it's from the RDA carrier term list of locally defined",
    )
    instanceFormats: Optional[List[InstanceFormat]] = Field(
        None, description='List of dereferenced instance formats'
    )
    physicalDescriptions: Optional[List[str]] = Field(
        None,
        description='Physical description of the described resource, including its extent, dimensions, and such other physical details as a description of any accompanying materials and unit type and size',
    )
    languages: Optional[List[str]] = Field(
        None, description='The set of languages used by the resource', min_items=0
    )
    notes: Optional[List[Note]] = Field(
        None, description='Bibliographic notes (e.g. general notes, specialized notes)'
    )
    administrativeNotes: Optional[List[str]] = Field(
        None, description='Administrative notes', min_items=0
    )
    modeOfIssuanceId: Optional[UUID4] = Field(
        None,
        description='UUID of the RDA mode of issuance, a categorization reflecting whether a resource is issued in one or more parts, the way it is updated, and whether its termination is predetermined or not (e.g. monograph,  sequential monograph, serial; integrating Resource, other)',
    )
    catalogedDate: Optional[str] = Field(
        None,
        description='Date or timestamp on an instance for when is was considered cataloged',
    )
    previouslyHeld: Optional[bool] = Field(
        False,
        description='Records the fact that the resource was previously held by the library for things like Hathi access, etc.',
    )
    staffSuppress: Optional[bool] = Field(
        None,
        description='Records the fact that the record should not be displayed for others than catalogers',
    )
    discoverySuppress: Optional[bool] = Field(
        False,
        description='Records the fact that the record should not be displayed in a discovery system',
    )
    statisticalCodeIds: Optional[List[str]] = Field(
        None, description='List of statistical code IDs', unique_items=True
    )
    sourceRecordFormat: Optional[SourceRecordFormat] = Field(
        None,
        description="Format of the instance source record, if a source record exists (e.g. FOLIO if it's a record created in Inventory,  MARC if it's a MARC record created in MARCcat or EPKB if it's a record coming from eHoldings)",
    )
    statusId: Optional[UUID4] = Field(
        None,
        description='UUID for the Instance status term (e.g. cataloged, uncatalogued, batch loaded, temporary, other, not yet assigned)',
    )
    statusUpdatedDate: Optional[str] = Field(
        None, description='Date [or timestamp] for when the instance status was updated'
    )
    tags: Optional[Tags] = Field(
        None, description='arbitrary tags associated with this instance', title='tags'
    )
    metadata: Optional[Metadata] = Field(
        None,
        description='Metadata about creation and changes to records, provided by the server (client should not provide)',
        title='Metadata Schema',
    )

    natureOfContentTermIds: Optional[List[NatureOfContentTermId]] = Field(
        None,
        description='Array of UUID for the Instance nature of content (e.g. bibliography, biography, exhibition catalogue, festschrift, newspaper, proceedings, research report, thesis or website)',
        unique_items=True,
    )

