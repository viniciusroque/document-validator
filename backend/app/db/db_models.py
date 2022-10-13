import datetime

import sqlalchemy
from sqlalchemy.ext import declarative as sa_declarative

from . import db_conf


BaseModel = sa_declarative.declarative_base()


def create_db():
    BaseModel.metadata.create_all(bind=db_conf.engine)


class LegalDocument(BaseModel):
    __tablename__ = "legal_documents"
    __table_args__ = (
        sqlalchemy.Index(
            "idx_legal_documents__document__type",
            "document",
            "type",
        ),
    )
    document: str = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        index=True,
        primary_key=True,
    )
    created_at_utc = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.utcnow,
    )

    # converter pra int
    # schema.DocumentTypeEnum
    type = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        index=True,
    )

    # converter pra int
    # schema.DocumentStatusEnum
    status = sqlalchemy.Column(
        sqlalchemy.String, nullable=False, index=True, default="ACTIVE"
    )
