from app.models import Role, StatusDevice, TypeDevice, Action, User
from app.core.enums import RoleType
from app.utils.password import hash_password 
from .data import ROLES, STATUS, TYPE_DEVICE, ACTIONS
from sqlalchemy import select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL")
DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD")
DEFAULT_ADMIN_FIRSTNAME = os.getenv("DEFAULT_ADMIN_FIRSTNAME")
DEFAULT_ADMIN_LASTNAME = os.getenv("DEFAULT_ADMIN_LASTNAME")


def seed_roles(db: Session):
    for data in ROLES:
        stmt = select(Role).where(Role.name == data["name"])
        exists = db.scalars(stmt).first()
        if exists is None:
            db.add(Role(**data))
            print("Seed : created " + data["name"])    

def seed_status(db: Session):
    for data in STATUS:
        stmt = select(StatusDevice).where(StatusDevice.name == data["name"])
        exists = db.scalars(stmt).first()
        if exists is None:
            db.add(StatusDevice(**data))
            print("Seed : created " + data["name"])    

def seed_type_device(db: Session):
    for data in TYPE_DEVICE:
        stmt = select(TypeDevice).where(TypeDevice.name == data["name"])
        exists = db.scalars(stmt).first()
        if exists is None:
            db.add(TypeDevice(**data))
            print("Seed : created " + data["name"])

def seed_actions(db: Session):
    for data in ACTIONS:
        stmt = select(Action).where(Action.name == data["name"])
        exists = db.scalars(stmt).first()
        if exists is None:
            db.add(Action(**data))
            print("Seed : created " + data["name"])

def seed_user(db: Session):
    stmt = select(User).where(User.email == DEFAULT_ADMIN_EMAIL)
    exists = db.scalars(stmt).first()
    if exists is None:
        db.add(User(
            email=DEFAULT_ADMIN_EMAIL, 
            password=hash_password(DEFAULT_ADMIN_PASSWORD),
            first_name=DEFAULT_ADMIN_FIRSTNAME,
            last_name=DEFAULT_ADMIN_LASTNAME,
            role_id=RoleType.ADMIN
        ))
        print("Seed : created admin user")
