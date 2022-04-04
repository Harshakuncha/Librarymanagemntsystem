
from app import db,login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  studentid=db.Column(db.String(20),nullable=False)
  studentname=db.Column(db.String(20),nullable=False)
  email=db.Column(db.String(20),nullable=False)
  contact=db.Column(db.String(20),nullable=False)
  books=db.relationship('Book', backref='owner',lazy=True)


class Book(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  bookid=db.Column(db.String(20),nullable=False)
  bookname=db.Column(db.String(30),nullable=False)
  author=db.Column(db.String(30),nullable=False)
  publisher=db.Column(db.String(30),nullable=False)
  copies=db.Column(db.Integer,nullable=False)
  issuedcopies=db.Column(db.Integer,default=0)
  issues=db.relationship('Issue',backref='issuedto',lazy=True)
  stob=db.relationship('bookstudent',backref='studentbook',lazy=True)
  # issue_id=db.Column(db.Integer,db.ForeignKey('issue.id'))
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

class bookstudent(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
  book_id=db.Column(db.Integer,db.ForeignKey('book.id'))
  bookid=db.Column(db.String(20))
  bookname=db.Column(db.String(30))
  studentid=db.Column(db.String(20))
  studentname=db.Column(db.String(20))
  count_ids=db.Column(db.Integer)


class Issue(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  date_created=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  type=db.Column(db.String,nullable=False)
  issuedcopies=db.Column(db.Integer,nullable=False)
  bookid=db.Column(db.String(20))
  bookname=db.Column(db.String(30))
  studentid=db.Column(db.String(20))
  studentname=db.Column(db.String(20))
  # bookissued=db.relationship('Book',backref='bookissue',lazy=True)
  book_id=db.Column(db.Integer,db.ForeignKey('book.id'))

class Admin(db.Model,UserMixin):
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(100),unique=True,nullable=False)
  email=db.Column(db.String(200),unique=True,nullable=False)
  password=db.Column(db.String(100),nullable=False)


