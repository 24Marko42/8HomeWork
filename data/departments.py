from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase

class Department(SqlAlchemyBase):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    chief = Column(Integer, nullable=False)
    members = Column(String)
    email = Column(String)
    
    def __repr__(self):
        return f"<Department> {self.title}"