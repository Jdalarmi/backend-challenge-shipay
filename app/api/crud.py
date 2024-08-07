from sqlalchemy.orm import Session
from passlib.context import CryptContext
import random
import string
from schemas import schemas
from models.users import User, Role
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password) if user.password else get_password_hash(''.join(random.choices(string.ascii_uppercase + string.digits, k=8)))
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role_id=user.role_id,
        created_at = datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_with_role_and_claims(db: Session, user_id: int):
    try:
        user = db.query(User).options(
            joinedload(User.role),
            joinedload(User.claims)
        ).filter(User.id == user_id).one()

        user_info = {
            "name": user.name,
            "email": user.email,
            "role_description": user.role.description if user.role else None,
            "claims": [{"description": claim.description} for claim in user.claims]
        }
        return user_info

    except NoResultFound:
        return None


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = Role(description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def role_exists(db: Session, role_id: int) -> bool:
    return db.query(Role).filter(Role.id == role_id).first() is not None