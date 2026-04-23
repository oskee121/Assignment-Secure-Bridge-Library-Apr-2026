from sqlalchemy import Column, Integer, String
from app.db import Base

class SecureRecord(Base):
    __tablename__ = "secure_records"

    id = Column(Integer, primary_key=True, index=True)

    encrypted_data = Column(String, nullable=False)
    iv = Column(String, nullable=False)
    blind_index = Column(String, index=True, nullable=False)

    key_version = Column(String, nullable=False)
    raw_data_for_demo_only = Column(String, nullable=False)
