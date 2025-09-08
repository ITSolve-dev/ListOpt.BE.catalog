from typing import Final

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

engine = create_engine("sqlite:///:memory:")
session: Final[scoped_session[Session]] = scoped_session(
    sessionmaker(bind=engine)
)
