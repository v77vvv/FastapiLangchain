from sqladmin import Admin, ModelView
from database.models import *

class UserAdmin(ModelView, model=UserProfile):
    column_list = [i.key for i in UserProfile.__mapper__.columns]

class UserRefreshAdmin(ModelView, model=UserRefresh):
    column_list = []

    for i in UserProfile.__mapper__.columns:
        column_list.append(i.key)