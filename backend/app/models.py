from sqlalchemy import Column, Integer, String
from app.db import Base

class SecureRecord(Base):
    __tablename__ = "secure_records"

    id = Column(Integer, primary_key=True, index=True)

    encrypted_blob = Column(String, nullable=False)  # JSON string
    blind_index = Column(String, index=True, nullable=False)

    key_version = Column(String, nullable=False)
