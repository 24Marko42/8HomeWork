import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyBase = declarative_base()
__factory = None
__engine = None

def global_init(db_file):
    global __factory, __engine
    if __factory:
        return
    
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    __engine = sa.create_engine(conn_str, echo=False)
    __factory = scoped_session(sessionmaker(bind=__engine))
    
    from . import users, jobs, departments
    SqlAlchemyBase.metadata.create_all(__engine)

def create_session():
    global __factory
    return __factory()

def get_engine():
    global __engine
    return __engine