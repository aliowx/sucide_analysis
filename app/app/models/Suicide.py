from datetime import datetime 
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    text,
    ARRAY,
    Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base



class Suicide(Base):
    uid: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    narrative_le: Mapped[str] = mapped_column(String, nullable=True)
    narrative_cme: Mapped[str] = mapped_column(String, nullable=True)
    depressed_mood: Mapped[str] = mapped_column(String, nullable=True)     