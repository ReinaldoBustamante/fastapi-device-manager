
from sqlalchemy import select,func, or_
from sqlalchemy.orm import Session
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self, limit: int, offset: int, search: str):
        query = select(User).where(User.is_active == True)
        if search:
            query = query.where(or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            ))
        total = self.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.limit(limit).offset(offset)
        result = self.db.scalars(query).all()
        return result, total
    
    def get_user_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = self.db.scalars(stmt).first()
        return result

    def get_user_by_email(self, user_email: str):
        query = select(User).where(User.email == user_email)
        result = self.db.scalars(query).first()
        return result

    def create_user(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user
    
    def patch_user(self, user: User, updates: dict):
        for key, value in updates.items():
            setattr(user, key, value)
        self.db.flush()
        return user