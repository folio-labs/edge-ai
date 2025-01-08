from typing import List, Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Field, UUID4

class ElectronicAccess(BaseModel):

    uri: str = Field(
        ...,
        description='uniform resource identifier (URI) is a string of characters designed for unambiguous identification of resources',
    )
    linkText: Optional[str] = Field(
        None,
        description='The value of the MARC tag field 856 2nd indicator, where the values are: no information provided, resource, version of resource, related resource, no display constant generated',
    )
    materialsSpecification: Optional[str] = Field(
        None,
        description='Materials specified is used to specify to what portion or aspect of the resource the electronic location and access information applies (e.g. a portion or subset of the item is electronic, or a related electronic resource is being linked to the record)',
    )
    publicNote: Optional[str] = Field(
        None, description='URL public note to be displayed in the discovery'
    )
    relationshipId: Optional[UUID4] = Field(
        None,
        description='UUID for the type of relationship between the electronic resource at the location identified and the item described in the record as a whole',
    )

class Note(BaseModel):
    instanceNoteTypeId: Optional[UUID4] = Field(None, description='ID of the type of note')
    note: Optional[str] = Field(None, description='Text content of the note')
    staffOnly: Optional[bool] = Field(
        False,
        description='If true, determines that the note should not be visible for others than staff',
    )

class Tags(BaseModel):
    tagList: Optional[List[str]] = Field(None, description='List of tags')