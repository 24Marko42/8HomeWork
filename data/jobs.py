from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship

class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey("users.id"), nullable=False)
    job = Column(String, nullable=False)
    work_size = Column(Integer, nullable=False)
    collaborators = Column(String)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    is_finished = Column(Boolean, default=False)
    
    leader = relationship("User")
    
    def __repr__(self):
        return f"<Job> {self.job}"