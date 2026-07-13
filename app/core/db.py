from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///managementTI.db', connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise 
    finally:
        db.close()
