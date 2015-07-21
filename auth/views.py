#encoding: utf8

from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.security import current_user

class UserAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class RoleAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')