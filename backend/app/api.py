import typing

import fastapi
from fastapi import responses, status

from . import schemas
from .services.legal_document_service import LegalDocumentServiceDb
from .db import db_conf, db_models

# TODO move to alembic
# Create DB
db_models.create_db()

_VERSION = "/api/v1"
_URL_PREFIX = f"{_VERSION}/legal_document"

app = fastapi.FastAPI(
    openapi_url=_VERSION + "/openapi.json",
    docs_url=_VERSION + "/docs",
)


def _get_db_session() -> db_conf.Session:
    db_session = db_conf.create_session()
    try:
        yield db_session
    finally:
        db_session.close()


def _get_service(
    session: db_conf.Session = fastapi.Depends(_get_db_session),
) -> LegalDocumentServiceDb:
    return LegalDocumentServiceDb(db_session=session)


@app.post(
    _URL_PREFIX,
    status_code=201,
    response_model=typing.Optional[schemas.DetailLegalDocument],
)
def create_legal_document(
    data: schemas.CreateLegalDocument,
    service: LegalDocumentServiceDb = fastapi.Depends(_get_service),
):

    doc = service.add(data)
    if not doc:
        return responses.JSONResponse(
            {},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return doc


@app.get(
    _URL_PREFIX + "/{document}",
    response_model=typing.Optional[schemas.DetailLegalDocument],
)
def detail_legal_document(
    document: schemas.DOCUMENT_FIELD,
    service: LegalDocumentServiceDb = fastapi.Depends(_get_service),
):
    doc = service.get(document=document)
    if not doc:
        return responses.JSONResponse(
            {},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return doc


@app.delete(
    _URL_PREFIX + "/{document}",
    response_model=schemas.DetailLegalDocument,
)
def delete_legal_document(
    document: schemas.DOCUMENT_FIELD,
    service: LegalDocumentServiceDb = fastapi.Depends(_get_service),
):
    doc = service.delete(document=document)
    if not doc:
        return responses.JSONResponse(
            {},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return doc


@app.put(
    _URL_PREFIX + "/{document}",
    response_model=schemas.DetailLegalDocument,
)
def update_legal_document(
    document: schemas.DOCUMENT_FIELD,
    data: schemas.UpdateDocument,
    service: LegalDocumentServiceDb = fastapi.Depends(_get_service),
):
    return service.update(document=document, data=data)


@app.get(
    _URL_PREFIX,
    response_model=schemas.FilterDocumentResponse,
)
def list_legal_document(
    filters: schemas.FilterLegalDocument = fastapi.Depends(
        schemas.FilterLegalDocument
    ),
    service: LegalDocumentServiceDb = fastapi.Depends(_get_service),
):
    return service.filter(filters)
