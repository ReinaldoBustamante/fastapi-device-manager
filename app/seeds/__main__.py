from app.core.db import SessionLocal
from .service import seed_roles, seed_status, seed_type_device, seed_actions, seed_user

def run():
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_status(db)
        seed_type_device(db)
        seed_actions(db)
        seed_user(db)
        db.commit()
        print("Seeds completed")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()