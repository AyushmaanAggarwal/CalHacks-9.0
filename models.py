from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

now = datetime.now()

association_table = db.Table(
    "Associate",
    db.Base.metadata,
    db.Column("user_id", db.ForeignKey("User.id"), primary_key=True),
    db.Column("protest_id", db.ForeignKey("Protest.id"), primary_key=True))


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_protests = db.relationship("Protest", back_populates="organizer")
    protest_list = db.relationship("Protest", secondary=association_table, back_populates="attendees")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(username):
        return User.query.get(username)


class Protest(db.Model):
    __tablename__ = "Protests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    location = db.Column(db.String(200))
    date = db.Column(db.datetime())
    attendees = db.relationship("User", secondary=association_table, back_populates="protest_list")
    organizer_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    organizer = db.relationship("User", back_populates='created_protests')

    @staticmethod
    def getPagination():
        return Protest.query.order_by(Protest.date).paginate(per_page=10)

    @staticmethod
    def get(id):
        return Protest.query.get(int(id))

    def addAttendee(self, username):
        user = User.get(username)
        self.attendees.append(user)
        user.protest_list.append(self)


class News(db.Model):
    __tablename__ = "News"
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(150))
    source = db.Column(db.String(150))
    date = db.Column(db.date())
    url = db.Column(db.String(150))

    @staticmethod
    def getPagination():
        return Protest.query.order_by(Protest.date).paginate(per_page=10)


