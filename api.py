from fastapi import FastAPI, Depends , status
from fastapi.middleware.cors import CORSMiddleware
from database.engin import engin
from database import models

from depends_functions import *

from routers.users import control as user_control
from routers.calories import control as calories_control

app = FastAPI()

app.include_router(user_control.router )
app.include_router(calories_control.router )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',status_code=status.HTTP_200_OK)
async def main():
    return ''

models.Base.metadata.create_all(bind=engin)
