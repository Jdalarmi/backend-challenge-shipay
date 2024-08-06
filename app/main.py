from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from schemas import schemas
from sqlalchemy.future import select
from api import crud
from db.connection import engine, Base, SessionLocal
from models.users import create_tables, User


create_tables()

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/users/{user_id}/", response_model=schemas.UserWithRoleAndClaims)
def get_user_with_role_and_claims(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_with_role_and_claims(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=List[schemas.UserOut])
def read_users():
    with SessionLocal() as session:
        query = session.query(User).options(
            joinedload(User.role),
            joinedload(User.claims)
        )
        users = query.all()
        return users

@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user


@app.post("/roles/", response_model=schemas.RoleResponse)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = crud.create_role(db=db, role=role)
    return db_role