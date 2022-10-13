from ..db import db_conf


class BaseServiceDB:
    db_session: db_conf.Session

    def __init__(self, db_session: db_conf.Session = None) -> None:
        self.db_session = db_session
