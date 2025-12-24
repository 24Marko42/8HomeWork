from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, configure_mappers
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

# Промежуточная таблица для связи многие-ко-многим (определяется ДО моделей)
jobs_to_categories = Table('jobs_to_categories', SqlAlchemyBase.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    modified_date = Column(DateTime, default=datetime.utcnow)
    
    # Связи (используем строковые имена для избежания циклических импортов)
    jobs = relationship("Jobs", back_populates="team_leader_user")
    departments = relationship("Department", back_populates="chief_user")
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"

class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey('users.id'), nullable=False)
    job = Column(String, nullable=False)
    work_size = Column(Integer, nullable=False)
    collaborators = Column(String)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_finished = Column(Boolean, default=False)
    
    # Связи
    team_leader_user = relationship("User", back_populates="jobs")
    categories = relationship(
        "Category",
        secondary=jobs_to_categories,
        back_populates="jobs"
    )
    
    def __repr__(self):
        return f"<Job> {self.job}"

class Department(SqlAlchemyBase):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    chief = Column(Integer, ForeignKey('users.id'), nullable=False)
    members = Column(String)
    email = Column(String, unique=True, nullable=False)
    
    # Связи
    chief_user = relationship("User", back_populates="departments")

class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    
    # Связи
    jobs = relationship(
        "Jobs",
        secondary=jobs_to_categories,
        back_populates="categories"
    )
    
    def __repr__(self):
        return f"<Category> {self.id} {self.name}"

# ЯВНО настраиваем мапперы после определения всех моделей
configure_mappers()