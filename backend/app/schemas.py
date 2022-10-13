import datetime
import enum

import pydantic
import pydantic.types
from .utils import utils_field


class BaseModel(pydantic.BaseModel):
    ...


class LegalDocumentTypeEnum(enum.Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"


DOCUMENT_FIELD = utils_field.DocumentField


class LegalDocument(BaseModel):
    document: DOCUMENT_FIELD


class CreateLegalDocument(LegalDocument):
    ...


class LegalDocumentStatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class DetailLegalDocument(LegalDocument):
    created_at_utc: datetime.datetime
    doc_type: LegalDocumentTypeEnum
    status: LegalDocumentStatusEnum


class UpdateDocument(BaseModel):
    status: LegalDocumentStatusEnum


class FilterOrderLegalDocumentEnum(enum.Enum):
    DOCUMENT_ASC = "DOCUMENT_ASC"
    DOCUMENT_DESC = "DOCUMENT_DESC"

    CREATION_ASC = "CREATION_ASC"
    CREATION_DESC = "CREATION_DESC"


class FilterLegalDocument(BaseModel):
    document_startswith: str = None
    document_contains: str = None
    document_equal: DOCUMENT_FIELD = None
    document_type: LegalDocumentTypeEnum = None
    order_by: FilterOrderLegalDocumentEnum = (
        FilterOrderLegalDocumentEnum.CREATION_DESC
    )
    page_size: pydantic.types.conint(gt=0) = 10
    page_number: pydantic.types.conint(gt=0) = 1


class FilterDocumentResponse(BaseModel):
    results: list[DetailLegalDocument]
    has_more_results: bool
