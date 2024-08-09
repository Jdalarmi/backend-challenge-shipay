from fastapi import APIRouter
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from schemas import shipay_schemas
from sqlalchemy.future import select
from api import shipay_crud
from db.connection import engine, Base, SessionLocal
from models.users import create_tables, User, Role
from fastapi.responses import JSONResponse

create_tables()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix= "/v1"
)

@router.get("/users/", response_model=List[shipay_schemas.UserOut])
def read_users():
    with SessionLocal() as session:
        query = session.query(User).options(
            joinedload(User.role),
            joinedload(User.claims)
        )
        users = query.all()
        return users

@router.get("/roles/{role_id}", response_model=shipay_schemas.RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/users/", response_model=shipay_schemas.UserCreate)
def create_user(user: shipay_schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if not shipay_crud.role_exists(db, user.role_id):
            links = {
                "create_role": shipay_schemas.Link(
                    href="/roles/v1/",
                    rel="create_role",
                    type="POST"
                )
            }
            error_response = shipay_schemas.ErrorResponse(
                error="Role not found. Please create a role first.",
                links=links
            )
            return JSONResponse(status_code=400, content=error_response.dict())

        shipay_crud.create_user(db=db, user=user)

        return JSONResponse(status_code=201, content={"success": "Successfully created user"})
    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
@router.post("/roles/", response_model=shipay_schemas.RoleResponse)
def create_role(role: shipay_schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = shipay_crud.create_role(db=db, role=role)
    return db_role
