from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self, limit: int, offset: int):
        stmt = select(User).limit(limit).offset(offset)
        users = self.db.scalars(stmt).all()
        total = self.db.scalar(
            select(func.count()).select_from(User)
        )

        return {
            "users": users,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        }
    
    def get_user_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = self.db.scalars(stmt).first()
        return result
    
    def update_user(self, user: User, update_data: dict):
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.refresh(user)
        return user
        