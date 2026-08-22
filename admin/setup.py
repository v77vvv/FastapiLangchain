from sqladmin import Admin 
from fastapi import FastAPI
from .views import *
from database.connection import create_async_engine

def admin_setup(app: FastAPI):
    admin = Admin(engine=create_async_engine, app=app)
    admin.add_view(UserAdmin)
    admin.add_view(UserRefreshAdmin)