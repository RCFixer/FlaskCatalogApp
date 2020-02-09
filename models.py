from flask_security import UserMixin, RoleMixin

from app import db


def slugify_name(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


roles_users = db.Table(
    'roles_users', db.Column('user_id', db.Integer(),
                             db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

site_tags = db.Table(
    'site_tags', db.Column('site_id', db.Integer(), db.ForeignKey('site.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.tag_id')))


class Site(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(250))
    short_url = db.Column(db.String(140))
    screenshot = db.Column(db.String(140))
    visits = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Site, self).__init__(*args, **kwargs)
        #self.generate_short_url()

    def generate_short_url(self):
        if self.name:
            self.short_url = slugify_name(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


class Tags(db.Model):
    tag_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    clear_name = db.Column(db.String(200))
    sites = db.relationship('Site',
                            secondary=site_tags,
                            backref=db.backref('tags', lazy='dynamic'))

    def __repr__(self):
        return '{}'.format(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Roles',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
