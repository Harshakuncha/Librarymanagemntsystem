
from flask import Flask,redirect,url_for,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SECRET_KEY']='Umavardhan@1'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///main3.db'
db=SQLAlchemy(app)

from flask_login import LoginManager,UserMixin,current_user,logout_user
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from datetime import datetime
from registrationform import Issueform, forgotform,studentdata,bookdata,LoginForm,RegisterForm,Returnform
from models import User,Admin,Book,Issue,bookstudent


 

@app.route('/')
@app.route('/admin',methods=['POST','GET'])
def admin():
  form=LoginForm()
  if form.validate_on_submit():
       usr=Admin.query.filter_by(email=form.email.data).first()
       if usr and (usr.password == form.password.data):
           next_page = request.args.get('next')
           return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('home'))
       else :
          flash('Please check email and password', 'danger')
  return render_template('admin.html',form=form)

@app.route('/adminregister',methods=['POST','GET'])
def adminregister():
  form=RegisterForm()
  if form.validate_on_submit():
    admin1=Admin(username=form.username.data,email=form.email.data,password=form.password.data)
    db.session.add(admin1)
    db.session.commit()
    flash(f'account created for {form.username.data}','success')
    return redirect(url_for('admin'))
  return render_template('adminregister.html',form=form)



@app.route('/home',methods=['POST','GET'])
def home():
  return render_template("home.html")

@app.route('/addbook',methods=['POST','GET'])
def addbook():
  return redirect(url_for('bookregister'))

@app.route('/studenttobook',methods=['POST','GET'])
def studenttobook():
  stob=bookstudent.query.all()
  d={}
  for x in stob:
    if x.studentname in d:
       d[x.studentname].append(x.bookid+":"+x.bookname+":"+str(x.count_ids))
    else:
       d[x.studentname]=[x.bookid+":"+x.bookname+":"+str(x.count_ids)]
  return render_template("studenttobook.html",stob=stob,d=d)


@app.route('/studentregister',methods=['POST','GET'])
def studentdataf():
  form=studentdata()
  if form.validate_on_submit():
    allusers=None
    user=User(studentid=form.studentid.data,studentname=form.studentname.data,email=form.email.data,contact=form.contact.data)
    db.session.add(user)
    db.session.commit()
    flash(f'Registered {form.studentname.data}','success')
    allusers=User.query.all()
    return render_template('studentdetails.html',form=form, allusers=allusers)
  allusers=User.query.all()
  return render_template('studentdata.html',form=form, allusers=allusers)



@app.route('/bookregister',methods=['POST','GET'])
def bookdataf():
  form=bookdata()
  allbooks=None
  if form.validate_on_submit():
     user=Book(bookid=form.bookid.data,bookname=form.bookname.data,author=form.author.data,publisher=form.publisher.data,copies=form.copies.data)
     db.session.add(user)
     db.session.commit()
     flash(f'Registered {form.bookname.data}','success')
     allbooks=Book.query.all()
     return render_template('viewbooks.html',form=form,allbooks=allbooks)
  allbooks=Book.query.all()
  return render_template('bookdata.html',form=form,allbooks=allbooks)

@app.route('/viewbooks',methods=['POST','GET'])
def viewbookaf():
   form=bookdata()
   allbooks=Book.query.all()
   return render_template('viewbooks.html',form=form,allbooks=allbooks)
 

@app.route('/details',methods=['POST','GET'])
def studentdetailsf():
  form=studentdata()
  allusers=User.query.all()
  stob=bookstudent.query.all()
  d={}
  for x in stob:
    if x.studentname in d:
       d[x.studentname].append(x.bookid+":"+x.bookname+":"+str(x.count_ids))
    else:
       d[x.studentname]=[x.bookid+":"+x.bookname+":"+str(x.count_ids)]
  return render_template('studentdetails.html',form=form,allusers=allusers,d=d,stob=stob)

@app.route('/issuedemo',methods=['POST','GET'])
def issuedemo():
  form=Issueform()
  return render_template('issue.html',form=form)

@app.route('/search',methods=['POST','GET'])
def searchf():
  form=Issueform()
  if form.validate_on_submit():
      
      flash(f'registered book with {form.bookid.data} ,to {form.studentid.data}','success')
      return redirect(url_for('home'))
  return render_template('search.html',form=form)

@app.route('/forgot',methods=['POST','GET'])
def forgotpasswordf():
  form=forgotform()
  cadmin=Admin.query.filter_by(email=form.email.data).first()
  if form.validate_on_submit():
    if cadmin and (cadmin.password==form.password.data):
      cadmin.password=form.confirm_password.data
      db.session.commit()
      flash("password changed successfully",'success')
      return redirect(url_for('admin'))
    else:
      flash("wrong email/password",'danger')
  return render_template("forgotpassword.html",form=form)


@app.route('/logout',methods=['POST','GET'])
def logout():
  logout_user()
  return redirect (url_for('admin'))

@app.route('/issue',methods=['POST','GET'])
def issue():
  form=Issueform()
  if form.validate_on_submit():
    bid=Book.query.filter_by(bookid=form.bookid.data).first()
    sid=User.query.filter_by(studentid=form.studentid.data).first()
    if bid and sid and (bid.copies>=int(form.copies.data)):
      # post_1=Book(bookid=bid.bookid,bookname=bid.bookname,author=bid.author,publisher=bid.publisher,copies=bid.copies-1,user_id=bid.id)
      # db.session.add(post_1)
      # db.session.delete(bid)
      # db.session.commit()
      bid.user_id=sid.id
      bstemp1=bookstudent.query.filter_by(user_id=sid.id).all()
      f=1
      if bstemp1 and f:
       for x in bstemp1:
        if (x.book_id==bid.id) and f:
         f=0
         x.count_ids+=int(form.copies.data)
         db.session.commit()
      if (f): 
        bs1=bookstudent(user_id=sid.id,book_id=bid.id,count_ids=int(form.copies.data),bookid=bid.bookid,studentid=sid.studentid,bookname=bid.bookname,studentname=sid.studentname)
        db.session.add(bs1)
        db.session.commit()

      bid.copies-=int(form.copies.data)
      bid.issuedcopies+=int(form.copies.data)
      db.session.commit()
      is1=Issue(issuedcopies=int(form.copies.data),type='Issued',book_id=bid.id,bookid=bid.bookid,studentid=sid.studentid,bookname=bid.bookname,studentname=sid.studentname)
      db.session.add(is1)
      db.session.commit()
      flash(f'Successfully issued {form.bookid.data} to {form.studentid.data}','success')
      return redirect(url_for('issue'))
    else:
      flash('check again ,one of the details entered is wrong','danger')
      return redirect(url_for('issue'))
  return render_template('issue.html',form=form)

@app.route('/return',methods=['POST','GET'])
def returnf():
  form=Returnform()
  if form.validate_on_submit():
    bid=Book.query.filter_by(bookid=form.bookid.data).first()
    sid=User.query.filter_by(studentid=form.studentid.data).first()
    bs1=bookstudent.query.filter_by(user_id=sid.id).all()
    currentissuedcopies=int(bid.issuedcopies)
    if bid and sid and (currentissuedcopies>=int(form.copies.data)):
      if bs1:

       for x in bs1:
         if x.book_id==bid.id:
           x.count_ids-=int(form.copies.data)

      bid.copies+=int(form.copies.data)
      bid.issuedcopies-=int(form.copies.data)
      
      db.session.commit()
      is1=Issue(issuedcopies=int(form.copies.data),type='Return',book_id=bid.id,bookid=bid.bookid,studentid=sid.studentid,bookname=bid.bookname,studentname=sid.studentname)
      db.session.add(is1)
      db.session.commit()
      flash('successfully returned','success')
      return render_template('home.html')
    else:
      flash("check details again",'danger')
  return render_template("return.html",form=form) 

 


@app.route('/transaction',methods=['POST','GET'])
def transaction():
  is1=Issue.query.all()
  return render_template('transaction.html',is1=is1)

@app.route('/viewlist',methods=['POST','GET'])
def viewlist():
  is1=Issue.query.all()
  return render_template('studentbooklist.html',is1=is1)

if __name__=='__main__':
    app.run()