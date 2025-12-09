from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship

class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    position = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship к задачам, где user — тимлид
    led_jobs = relationship("Jobs", back_populates="leader")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        # как просили: <Colonist> {id} {surname} {name}
        s = self.surname if self.surname else ""
        return f"<Colonist> {self.id} {s} {self.name}"
