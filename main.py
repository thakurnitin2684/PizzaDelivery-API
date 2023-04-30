from fastapi import FastAPI
from routers.auth_routes import auth_router
from routers.order_routes import order_router
from database import engine
import models


app=FastAPI()
models.Base.metadata.create_all(engine) 


app.include_router(auth_router)
app.include_router(order_router)


