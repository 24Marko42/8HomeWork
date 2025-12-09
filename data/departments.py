from sqlalchemy import Column, Integer, String, JSON
from .db_session import SqlAlchemyBase

class Department(SqlAlchemyBase):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    chief = Column(Integer, nullable=True)  # id руководителя
    members = Column(JSON, nullable=True)   # список id
    email = Column(String, nullable=True)

    def __repr__(self):
        return f"<Department> {self.title}"
