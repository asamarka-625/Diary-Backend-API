from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
import sqlalchemy.orm as so
import sqlalchemy as sa
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional


class Base(AsyncAttrs, so.DeclarativeBase):
    def update_from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)              
                
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        

# Модель записи в ежедневнике
class DiaryEntry(Base):
    __tablename__ = "diary_entries"
    
    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    content: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now(), index=True, nullable=True)
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(timezone=True), onupdate=func.now())
    is_completed: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False, index=True)
    
    def __repr__(self):
        return f"<DiaryEntry {self.title}>"