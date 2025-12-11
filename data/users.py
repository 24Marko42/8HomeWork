from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    modified_date = Column(DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        s = self.surname if self.surname else ""
        return f"<Colonist> {self.id} {s} {self.name}"