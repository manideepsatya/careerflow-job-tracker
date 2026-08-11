from sqlalchemy import Column, Integer, String

from database import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    location = Column(String, nullable=False)
    job_url = Column(String, nullable=False)
    status = Column(String, nullable=False)