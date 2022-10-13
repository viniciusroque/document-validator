import typing
import sqlalchemy

from .. import schemas
from ..db import db_models
from . import base_service


def _db_model_to_schema(
    legal_document: db_models.LegalDocument,
) -> schemas.DetailLegalDocument:
    return schemas.DetailLegalDocument(
        document=legal_document.document,
        created_at_utc=legal_document.created_at_utc,
        doc_type=legal_document.type,
        status=legal_document.status,
    )


_QUERY_ORDER_MAPPING = {
    schemas.FilterOrderLegalDocumentEnum.DOCUMENT_ASC: db_models.LegalDocument.document.asc(),
    schemas.FilterOrderLegalDocumentEnum.DOCUMENT_DESC: db_models.LegalDocument.document.desc(),
    schemas.FilterOrderLegalDocumentEnum.CREATION_ASC: db_models.LegalDocument.created_at_utc.asc(),
    schemas.FilterOrderLegalDocumentEnum.CREATION_DESC: db_models.LegalDocument.created_at_utc.desc(),
}


class LegalDocumentServiceDb(base_service.BaseServiceDB):
    def _get_document_by_document(self, document):
        query = self.db_session.query(db_models.LegalDocument).filter(
            db_models.LegalDocument.document == document,
        )
        return query.first()

    def add(
        self, data: schemas.CreateLegalDocument
    ) -> typing.Optional[schemas.DetailLegalDocument]:
        document_type = schemas.LegalDocumentTypeEnum.CPF.value
        if len(data.document) != 11:
            document_type = schemas.LegalDocumentTypeEnum.CNPJ.value

        try:
            doc = db_models.LegalDocument(
                document=data.document, type=document_type
            )
            self.db_session.add(doc)
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.db_session.rollback()
            return None

        return _db_model_to_schema(doc)

    def get(
        self, document: schemas.DOCUMENT_FIELD
    ) -> typing.Optional[schemas.DetailLegalDocument]:
        doc = self._get_document_by_document(document)
        if not doc:
            return None

        return _db_model_to_schema(doc)

    def delete(
        self, document: schemas.DOCUMENT_FIELD
    ) -> typing.Optional[schemas.DetailLegalDocument]:
        doc = doc = self._get_document_by_document(document)
        if not doc:
            return None

        self.db_session.delete(doc)
        self.db_session.commit()

        return _db_model_to_schema(doc)

    def update(
        self,
        document: schemas.DOCUMENT_FIELD,
        data: schemas.UpdateDocument,
    ) -> typing.Optional[schemas.DetailLegalDocument]:
        doc = self._get_document_by_document(document)
        doc.status = data.status.value
        self.db_session.commit()

        return _db_model_to_schema(doc)

    def filter(
        self, filters: schemas.FilterLegalDocument
    ) -> schemas.FilterDocumentResponse:
        query = self.db_session.query(db_models.LegalDocument)

        if filters.document_startswith:
            query = query.filter(
                db_models.LegalDocument.document.startswith(
                    filters.document_startswith
                )
            )
        if filters.document_contains:
            query = query.filter(
                db_models.LegalDocument.document.contains(
                    filters.document_contains
                )
            )
        if filters.document_equal:
            query = query.filter(
                db_models.LegalDocument.document == filters.document_equal
            )

        if filters.document_type:
            query = query.filter(
                db_models.LegalDocument.type == filters.document_type.value
            )

        query = query.order_by(_QUERY_ORDER_MAPPING[filters.order_by])

        query = query.offset(
            (filters.page_number - 1) * filters.page_size
        ).limit(filters.page_size + 1)

        all_results = query.all()
        has_more_results = len(all_results) > filters.page_size

        results = all_results[: filters.page_size]
        return schemas.FilterDocumentResponse(
            results=[_db_model_to_schema(r) for r in results],
            has_more_results=has_more_results,
        )
