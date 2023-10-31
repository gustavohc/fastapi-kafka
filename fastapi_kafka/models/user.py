from sqlalchemy import Boolean, Column, Integer, String

from fastapi_kafka.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
