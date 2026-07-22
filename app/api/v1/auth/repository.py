from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, username: str):
        stmt = select(User).where(User.email == username)
        result = self.db.scalars(stmt).first()
        return result
   
    def create_user(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user
    