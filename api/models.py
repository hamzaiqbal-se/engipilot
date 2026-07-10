from sqlalchemy import Column, Integer, String
from api.database import Base

class ConnectionTest(Base):
    __tablename__ = "connection_test"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, default="EngiPilot is connected!")