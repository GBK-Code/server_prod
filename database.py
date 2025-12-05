from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import String, Integer, Column, UniqueConstraint
import os

DB_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    DB_URL,
    connect_args={"sslmode": "required"},
    pool_pre_ping=True
)


class Base(DeclarativeBase):
    pass


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    title = Column(String)
    details = Column(String)

    __table_args__ = (
        UniqueConstraint(
            "title", "details",
            name="uq_title_details"
        ), # <--- comma defines __table_args__ as tuple
    )

SessionLocal = sessionmaker(autoflush=False, bind=engine)
