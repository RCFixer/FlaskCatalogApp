from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin, expose
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from flask import redirect, url_for, request

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/', methods=('GET', 'POST'))
    def add_site(self):
        if request.method == 'POST':
            site_name = request.form.get('site_name')
            site_url = request.form.get('site_url')
            site_screenshot = request.form.get('screenshot')
            site_tags = request.form.getlist('tags')
            site = Site(name=site_name,
                        url=site_url,
                        screenshot=site_screenshot,
                        tags=site_tags)
        tags = Tags.query.all()
        return self.render('add_site.html', tags=tags)


admin = Admin(app,
              'Katalog',
              url='/',
              index_view=HomeAdminView(name='Добавить сайт'))
admin.add_view(BaseModelView(Site, db.session))
admin.add_view(BaseModelView(Tags, db.session))
admin.add_view(BaseModelView(User, db.session))
admin.add_view(BaseModelView(Roles, db.session))

### Flask-security ###

user_datastore = SQLAlchemyUserDatastore(db, User, Roles)
security = Security(app, user_datastore)
