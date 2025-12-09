import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyBase = declarative_base()
__engine = None
__Session = None

def global_init(db_file):
    global __engine, __Session
    if __engine:
        return
    conn_str = f"sqlite:///{db_file}"
    __engine = sqlalchemy.create_engine(conn_str, echo=False, connect_args={"check_same_thread": False})
    __Session = scoped_session(sessionmaker(bind=__engine))

def create_session():
    global __Session
    if __Session is None:
        raise Exception("Call global_init() before create_session()")
    return __Session()

def get_engine():
    return __engine
