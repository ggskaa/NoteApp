from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, Column
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///notes.db')
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass


class Notes_model(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    createdAT: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updatedAT: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)
