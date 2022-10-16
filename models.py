from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

now = datetime.now()

association_table = db.Table(
    "Associate",
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
    def get(i_username):
        return User.query.filter_by(username=i_username).first()


class Protest(db.Model):
    __tablename__ = "Protest"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    location = db.Column(db.String(200))
    date = db.Column(db.String(20))
    attendees = db.relationship("User", secondary=association_table, back_populates="protest_list")
    organizer_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    organizer = db.relationship("User", back_populates='created_protests')

    @staticmethod
    def getPagination(page_num):
        return Protest.query.order_by(Protest.id).paginate(page=int(page_num), per_page=10, error_out=False).items

    @staticmethod
    def get(i_id):
        return Protest.query.filter_by(id=int(i_id)).first()

    def addAttendee(self, username):
        user = User.get(username)
        self.attendees.append(user)
        user.protest_list.append(self)


class News(db.Model):
    __tablename__ = "News"
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(150))
    source = db.Column(db.String(150))
    date = db.Column(db.String(20))
    url = db.Column(db.String(150))

    @staticmethod
    def getPagination(page_num):
        return News.query.order_by(News.date).paginate(page=int(page_num), per_page=10, error_out=False).items


    @staticmethod
    def get(i_id):
        return News.query.filter_by(id=int(i_id)).first()


#db.create_all()
#db.drop_all()

'''news_1 = News(headline="Iran protests: Iran's Gen Z 'realise life can be lived differently'", source="BBC News", date=datetime(2022,10,14,16,00,00), url="https://www.bbc.com/news/world-middle-east-63213745")
news_2 = News(headline="What’s Driving the Protests in Iran?", source="NYTimes", date=datetime(2022,9,24,12,00,00), url="https://www.nytimes.com/2022/09/22/world/middleeast/iran-protests.html")
db.session.add(news_1)
db.session.add(news_2)
db.session.commit()'''

#news = News.get(3)
#news1 = News.get(4)
#news.title="New Berkeley Protest for People's Park"
#news1.title="Protests in Myanmar from last year"
#db.session.commit()
