import sqlalchemy
import sqlalchemy.orm

from .. import constants


engine = sqlalchemy.create_engine(
    constants.SQLALCHEMY_DATABASE_URL,
    echo=constants.DEBUG,
)

_SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Session = sqlalchemy.orm.Session


def create_session() -> Session:
    return _SessionLocal()
