from fastapi import FastAPI
from sqladmin import Admin
from app.admin.auth import authentication_backend
from app.db.database import db_helper
from . import sqladmin


def setup_admin(app: FastAPI):
    admin = Admin(app=app, engine=db_helper.engine, authentication_backend=authentication_backend)
    admin.add_view(sqladmin.StudentAdmin)
    admin.add_view(sqladmin.SponsorAdmin)
