from sqlalchemy.orm import Session


class BaseRespository:
    def __init__(self, conn: Session):
        self._conn = conn

    @property
    def connection(self) -> Session:
        return self._conn
