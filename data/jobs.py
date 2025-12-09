# data/jobs.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from datetime import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship

class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey("users.id"), nullable=False)
    job = Column(String, nullable=False)
    work_size = Column(Integer, nullable=False, default=0)
    collaborators = Column(JSON, nullable=True)  # список id участников
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_finished = Column(Boolean, default=False)

    leader = relationship("User", back_populates="led_jobs")

    def __repr__(self):
        return f"<Job> {self.job}"
