from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4, ConfigDict

class Metadata(BaseModel):
    model_config = ConfigDict(extra='forbid')

    createdDate: datetime = Field(
        ..., description='Date and time when the record was created'
    )
    createdByUserId: UUID4 = Field(
        None, description='ID of the user who created the record (when available)'
    )
    createdByUsername: Optional[str] = Field(
        None, description='Username of the user who created the record (when available)'
    )
    updatedDate: Optional[datetime] = Field(
        None, description='Date and time when the record was last updated'
    )
    updatedByUserId: Optional[UUID4] = Field(
        None, description='ID of the user who last updated the record (when available)'
    )
    updatedByUsername: Optional[str] = Field(
        None,
        description='Username of the user who last updated the record (when available)',
    )
