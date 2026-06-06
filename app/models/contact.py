from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
