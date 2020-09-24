from flask_login import UserMixin
import pendulum
from werkzeug.security import check_password_hash, generate_password_hash

from bytardag import db, login


class Permission:
    REGISTER_SHEETS = 0x01
    ADMINISTER = 0x80


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    @staticmethod
    def insert_roles():
        """Method for setting roles for user accounts if they are missing.
        Teacher-permissions is default.
        """
        roles = {
            "Volunteer": (Permission.REGISTER_SHEETS, True),
            "Administrator": (0xFF, False),
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=pendulum.now)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    sheets = db.relationship(
        "Sheet", foreign_keys="Sheet.owned_by", backref="owner", lazy="dynamic"
    )
    signed_sheets = db.relationship(
        "Sheet", foreign_keys="Sheet.signed_by", backref="signee", lazy="dynamic"
    )

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Row(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    seller = db.Column(db.String(4), index=True)
    amount = db.Column(db.Integer())
    sheet_id = db.Column(db.Integer(), db.ForeignKey("sheet.id"))
    timestamp = db.Column(db.DateTime, index=True, default=pendulum.now)

    def __repr__(self):
        return "<Row {}>".format(self.id)


class Sheet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(4), index=True)
    rows = db.relationship("Row", backref="sheet", lazy="dynamic")
    timestamp = db.Column(db.DateTime, index=True, default=pendulum.now)
    closed = db.Column(db.DateTime, index=True, default=None)
    signed_at = db.Column(db.DateTime, index=True, default=None)
    owned_by = db.Column(db.Integer(), db.ForeignKey("user.id"))
    signed_by = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Sheet {}>".format(self.id)


class Seller(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    seller_id = db.Column(db.String(4), index=True, unique=True)

    def __repr__(self):
        return "<Seller {}>".format(self.id)
