from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Umavardhan@1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main3.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'vardhanr009@gmail.com'
app.config['MAIL_PASSWORD'] = 'Umavardhan@1'
mail = Mail(app)
db = SQLAlchemy(app)
from flask_login import LoginManager, logout_user  # noqa: E402
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from registrationform import Issueform, forgotform, studentdata, \
  bookdata, LoginForm, RegisterForm, Returnform  # noqa: E402
from models import User, Admin, Book, Issue, bookstudent  # noqa: E402

# librarymanagament system


@app.route('/')
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    '''

    This is a admin function where it does the
    authentication work ,it checks with the
    database if he is a admin then we can login
    to see the dashboard.

    '''
    form = LoginForm()
    if form.validate_on_submit():
        usr = Admin.query.filter_by(email=form.email.data).first()
        if usr and (usr.password == form.password.data):
            next_page = request.args.get('next')
            return redirect(url_for(next_page[1:])) if next_page else \
                redirect(url_for('home'))
        else:
            flash('Please check email and password', 'danger')
    return render_template('admin.html', form=form)


@app.route('/adminregister', methods=['POST', 'GET'])
def adminregister():
    '''
    This function take in values and
    create a tuple and make the admin
    to register in the library system.

    '''
    form = RegisterForm()
    if form.validate_on_submit():
        admin1 = Admin(username=form.username.data,
                       email=form.email.data, password=form.password.data)
        db.session.add(admin1)
        db.session.commit()
        flash(f'account created for {form.username.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('adminregister.html', form=form)


@app.route('/home', methods=['POST', 'GET'])
def home():
    '''
    This function takes you to view the dashboard.

    '''
    return render_template("home.html")


@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    '''
    This function is redirect to register a book in a library.

    '''
    return redirect(url_for('bookregister'))


@app.route('/studenttobook', methods=['POST', 'GET'])
def studenttobook():
    '''
    This function takes all student to
    book relations and output them in
    a dictionary manner.

    Args:

    1:Fetching all student to book relations

    2:If there isn't one then creating a key with empty
      value else adding the value i.e book to the
      student and passing to studenttobook function

    '''
    stob = bookstudent.query.all()
    d = {}
    for x in stob:
        if x.studentname in d:
            d[x.studentname].append(x.bookid + ":"
                                    + x.bookname + ":" + str(x.count_ids))
        else:
            d[x.studentname] = [x.bookid + ":" +
                                x.bookname + ":" + str(x.count_ids)]
    return render_template("studenttobook.html", stob=stob, d=d)


@app.route('/studentregister', methods=['POST', 'GET'])
def studentdataf():
    '''
    This function take in details of the student
    and register him in the library system.

    '''
    form = studentdata()
    if form.validate_on_submit():
        allusers = None
        user = User(studentid=form.studentid.data,
                    studentname=form.studentname.data,
                    email=form.email.data, contact=form.contact.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Registered {form.studentname.data}', 'success')
        allusers = User.query.all()
        return render_template('studentdetails.html',
                               form=form, allusers=allusers)
    allusers = User.query.all()
    return render_template('studentdata.html', form=form, allusers=allusers)


@app.route('/bookregister', methods=['POST', 'GET'])
def bookdataf():
    '''
    This function take details of the book and register it in system.

    '''
    form = bookdata()
    allbooks = None
    if form.validate_on_submit():
        user = Book(bookid=form.bookid.data, bookname=form.bookname.data,
                    author=form.author.data,
                    publisher=form.publisher.data,
                    copies=form.copies.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Registered {form.bookname.data}', 'success')
        allbooks = Book.query.all()
        return render_template('viewbooks.html', form=form, allbooks=allbooks)
    allbooks = Book.query.all()
    return render_template('bookdata.html', form=form, allbooks=allbooks)


@app.route('/viewbooks', methods=['POST', 'GET'])
def viewbookaf():
    '''
    This is function where we can view all the books
    in the system with and the deatails of it.

    '''
    form = bookdata()
    allbooks = Book.query.all()
    return render_template('viewbooks.html', form=form, allbooks=allbooks)


@app.route('/details', methods=['POST', 'GET'])
def studentdetailsf():
    form = studentdata()
    allusers = User.query.all()
    stob = bookstudent.query.all()
    d = {}
    for x in stob:
        if x.studentname in d:
            d[x.studentname].append(x.bookid + ":"
                                    + x.bookname + ":" + str(x.count_ids))
        else:
            d[x.studentname] = [x.bookid + ":"
                                + x.bookname + ":" + str(x.count_ids)]
    return render_template('studentdetails.html', form=form,
                           allusers=allusers, d=d, stob=stob)


@app.route('/issuedemo', methods=['POST', 'GET'])
def issuedemo():
    form = Issueform()
    return render_template('issue.html', form=form)


@app.route('/search', methods=['POST', 'GET'])
def searchf():
    form = Issueform()
    if form.validate_on_submit():
        flash('registered book with'+str(form.bookid.data)
              + "to" + str(form.studentid.data), 'success')
        return redirect(url_for('home'))
    return render_template('search.html', form=form)


@app.route('/forgot', methods=['POST', 'GET'])
def forgotpasswordf():
    form = forgotform()
    cadmin = Admin.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if cadmin and (cadmin.password == form.password.data):
            cadmin.password = form.confirm_password.data
            db.session.commit()
            flash("password changed successfully", 'success')
            return redirect(url_for('admin'))
    else:
        flash("wrong email/password", 'danger')
    return render_template("forgotpassword.html", form=form)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('admin'))


@app.route('/issue', methods=['POST', 'GET'])
def issue():
    '''
    This function is a desired function to issue
    a book to a student along with number of copies
    to be issued
    Args:

    1.Issue a book-Action

    2.On submit it custom checks weather the transaction
      is possible or not and then show a flash message accordingly

    3.On successful submission it send a email from
      admin to the user stating that the book is issued along
      with number of copies

    '''
    form = Issueform()
    if form.validate_on_submit():
        bid = Book.query.filter_by(bookid=form.bookid.data).first()
        sid = User.query.filter_by(studentid=form.studentid.data).first()
        if bid and sid and (bid.copies >= int(form.copies.data)):
            bid.user_id = sid.id
            bstemp1 = bookstudent.query.filter_by(user_id=sid.id).all()
            f = 1
            if bstemp1 and f:
                for x in bstemp1:
                    if (x.book_id == bid.id) and f:
                        f = 0
                        x.count_ids += int(form.copies.data)
                        db.session.commit()
            if (f):
                bs1 = bookstudent(user_id=sid.id,
                                  book_id=bid.id,
                                  count_ids=int(form.copies.data),
                                  bookid=bid.bookid,
                                  studentid=sid.studentid,
                                  bookname=bid.bookname,
                                  studentname=sid.studentname)
                db.session.add(bs1)
                db.session.commit()
            msg = Message('Hello,Issued a new book',
                          body="Bookname" + " " + bid.bookname + " "
                          "and number of copies issued are in total are"
                          + str(form.copies.data),
                          sender='vardhanr009@gmail.com',
                          recipients=[sid.email])
            mail.send(msg)
            bid.copies -= int(form.copies.data)
            bid.issuedcopies += int(form.copies.data)
            db.session.commit()
            is1 = Issue(issuedcopies=int(form.copies.data),
                        type='Issued',
                        book_id=bid.id,
                        bookid=bid.bookid,
                        studentid=sid.studentid,
                        bookname=bid.bookname,
                        studentname=sid.studentname)
            db.session.add(is1)
            db.session.commit()
            flash(f'Successfully issued {form.bookid.data} to \
            {form.studentid.data}', 'success')
            return redirect(url_for('issue'))
        else:
            flash('check again ,one of the details entered is wrong', 'danger')
            return redirect(url_for('issue'))
    return render_template('issue.html', form=form)


@app.route('/return', methods=['POST', 'GET'])
def returnf():
    form = Returnform()
    if form.validate_on_submit():
        bid = Book.query.filter_by(bookid=form.bookid.data).first()
        sid = User.query.filter_by(studentid=form.studentid.data).first()
        bs1 = bookstudent.query.filter_by(user_id=sid.id).all()
        currentissuedcopies = int(bid.issuedcopies)
        if bid and sid and (currentissuedcopies >= int(form.copies.data)):
            if bs1:
                for x in bs1:
                    if x.book_id == bid.id:
                        x.count_ids -= int(form.copies.data)

            bid.copies += int(form.copies.data)
            bid.issuedcopies -= int(form.copies.data)
            db.session.commit()
            is1 = Issue(issuedcopies=int(form.copies.data),
                        type='Return', book_id=bid.id, bookid=bid.bookid,
                        studentid=sid.studentid, bookname=bid.bookname,
                        studentname=sid.studentname)
            db.session.add(is1)
            db.session.commit()
            msg = Message('Hello,Retured a new book',
                          body="Bookname"+" "+bid.bookname + " "
                          + "and number of copies returned are in total are "
                          + str(form.copies.data),
                          sender='vardhanr009@gmail.com',
                          recipients=[sid.email])
            mail.send(msg)
            flash('successfully returned', 'success')
            return render_template('home.html')
        else:
            flash("check details again", 'danger')
    return render_template("return.html", form=form)


@app.route('/transaction', methods=['POST', 'GET'])
def transaction():
    is1 = Issue.query.all()
    return render_template('transaction.html', is1=is1)


@app.route('/viewlist', methods=['POST', 'GET'])
def viewlist():
    is1 = Issue.query.all()
    return render_template('studentbooklist.html', is1=is1)


if __name__ == '__main__':
    app.run()
