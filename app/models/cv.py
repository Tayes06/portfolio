from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from app.database import Base


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
