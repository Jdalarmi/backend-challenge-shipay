from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class UserCreate(BaseModel):
    name: str
    email: str
    role_id: int
    password: Optional[str] = None

class Claim(BaseModel):
    description: str

class UserWithRoleAndClaims(BaseModel):
    name: str
    email: str
    role_description: str
    claims: List[Claim]

class RoleCreate(BaseModel):
    description: str

class RoleResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True

class ClaimOut(BaseModel):
    id: int
    description: str
    active: bool

    class Config:
        orm_mode = True

class RoleOut(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: RoleOut
    claims: List[ClaimOut]

    class Config:
        orm_mode = True

class Link(BaseModel):
    href: str
    rel: str
    type: str

class ErrorResponse(BaseModel):
    error: str
    links: Dict[str, Link] = Field(default_factory=dict)