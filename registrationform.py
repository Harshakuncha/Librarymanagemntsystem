
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo,ValidationError,Email
# from models import User
class studentdata(FlaskForm):
    studentid = StringField('STUDENT_ID',
                           validators=[DataRequired(), Length(min=2, max=20)])
    studentname = StringField('STUDENT_NAME',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    contact = StringField('CONTACT', validators=[DataRequired()])
    
    submit = SubmitField('Add student')

class bookdata(FlaskForm):
    bookid = StringField('BOOK_ID',
                           validators=[DataRequired(), Length(min=2, max=20)])
    bookname = StringField('BOOK_NAME',
                           validators=[DataRequired(), Length(min=2, max=20)])
    author= StringField('AUTHOR',
                        validators=[DataRequired()])
    publisher = StringField('PUBLISHER', validators=[DataRequired()])
    copies=StringField('COPIES',validators=[DataRequired()])
    
    submit = SubmitField('Add Book')

  
class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember= BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField('Username',
             validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email',
            validators=[DataRequired(),Length(min=6, max=40)])
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password= PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')])
    submit=SubmitField('signup')

class Issueform(FlaskForm):
        bookid=StringField('BOOK_ID',validators=[DataRequired()])
        studentid=StringField('STUDENT_ID',validators=[DataRequired()])
        copies=StringField('COPIES',validators=[DataRequired()])
        submit=SubmitField('Issue')

class Returnform(FlaskForm):
        bookid=StringField('BOOK_ID',validators=[DataRequired()])
        studentid=StringField('STUDENT_ID',validators=[DataRequired()])
        copies=StringField('COPIES',validators=[DataRequired()])
        submit=SubmitField('Return')


class forgotform(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(),Length(min=6, max=40)])
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password= PasswordField('New password',
            validators=[DataRequired(), Length(min=8,max=64)])
    submit=SubmitField('Change password')
        
