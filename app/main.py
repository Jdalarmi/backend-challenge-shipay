from fastapi import FastAPI
from routes import shipay_routes
from db.connection import engine, Base
from models.users import create_tables

create_tables()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SHIPAY - CHALLENGE",
    description="Backend challenge.",
    version="1.0.0",
)

app.include_router(shipay_routes.router)