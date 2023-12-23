from flask import Flask, render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired, EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user,LoginManager,login_required,logout_user,current_user
# creating a flask instance
app = Flask(__name__)
# we create a secret key so that in future externally no one can make changes
app.config['SECRET_KEY']="MY_KEY"

# creating data base for our website, OLD SQLite DB
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# New MySQL DB -># app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:neetu324@localhost/our_users'
# Initialize the data base
db=SQLAlchemy(app)
migrate=Migrate(app,db)

# FLASK LOGIN REQUIRED THINGS
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# create login form
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Submit")

# creating login page
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        # finding the user with that username
        user=Users.query.filter_by(username=form.username.data).first()
        # if user exist
        if user:
            # if user found we need to check if passwords match or not
            if check_password_hash(user.password_hash,form.password.data):
                # if passwords match
                login_user(user)
                # flash('Logged in Succesfullly !')
                return redirect(url_for('dashboard'))
            else:
                # password does not match
                flash('wrong password!, try again')
        else:
            flash("No such user exists!")
    return render_template('login.html',form=form)


# creating a logout page
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    flash('Log out!')
    logout_user()
    return redirect(url_for('login'))  


# creating Dashboard
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id=current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name=request.form['name']
        name_to_update.email=request.form['email']
        name_to_update.favourite_color=request.form['favourite_color']
        name_to_update.username=request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash("Try again!")
            return render_template("dashboard.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("dashboard.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id= id)
    return render_template('dashboard.html')


# creating a blog post model
class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    author=db.Column(db.String(230))
    content=db.Column(db.Text)
    title=db.Column(db.String(230))
    date_posted=db.Column(db.DateTime, default=datetime.utcnow)
    slug=db.Column(db.String(225))
@app.route('/post/<int:id>')
def post(id):
    post=Posts.query.get_or_404(id)
    return render_template('post.html',post=post)
# create a Post form
class PostForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    content=StringField("Content",validators=[DataRequired()],widget=TextArea())
    author=StringField("Author",validators=[DataRequired()])
    slug=StringField("Slug",validators=[DataRequired()])
    submit=SubmitField("Submit")

# add post page
@app.route('/add-post', methods=['GET','POST'])
# @login_required
def add_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
        
        # clear the form
        form.title.data=''
        form.content.data=''
        form.author.data=''
        form.slug.data=''
        
        # add to data base
        db.session.add(post)
        db.session.commit()
        
        # Return a message
        flash("Blog post submitted!")
        
    # redirect to page
    return render_template("add_post.html",form=form)
@app.route('/posts')
def posts():
    # taking all the post 
    posts=Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html",posts=posts)
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post=Posts.query.get_or_404(id)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.author=form.author.data
        post.slug=form.slug.data
        post.content=form.content.data
        # update database
        db.session.add(post)
        db.session.commit()
        flash("Updated succesfully")
        # redirecting to post page
        return redirect(url_for('post',id=post.id))
    form.title.data=post.title
    form.author.data=post.author
    form.slug.data=post.slug
    form.content.data=post.content
    return render_template('edit_post.html',form=form)
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete=Posts.query.get_or_404(id)
    post_to_delete.title=None
    post_to_delete.author=None
    post_to_delete.slug=None
    post_to_delete.content=None
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Blog Deleted!")
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)
    except:
        flash("Oops! something went wrong please try again...")
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)


    
# Json
@app.route('/date')
def get_current_date():
    favourite_anime={
        "nits" :"Metal_Alchemist",
        "kT" : "JJK",
        "MS" : "AOT"
    }
    # return favourite_anime
    return {"Date": date.today()}
    # creating a model
class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),nullable=False,unique=True)
    name=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    favourite_color=db.Column(db.String(200))
    date_added=db.Column(db.DateTime,default=datetime.utcnow)
    password_hash=db.Column(db.String(200))
    @property
    def password(self):
        raise AttributeError('Password Attribute is not readable!')
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    # creating a String
    # The __repr__ method in Python is a special method used to define a string representation of an object.
    def __repr__(self):
        return '<Name %r>' %self.name
class UserForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    username=StringField("Username", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    favourite_color=StringField("Favourite Colour")
    password_hash=PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2','Password must match!')])
    password_hash2=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField("Submit")
@app.route('/delete/<int:id>')
def delete(id):
    form=UserForm()
    name=None
    user_to_delete=Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted!")
        our_users=Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("Oops something went wrong try again later!")
        our_users=Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=str(form.email.data)).first()

        if user is None:
            # before putting the password we want to hash the password so
            hashed_pw=generate_password_hash(form.password_hash.data)
            user = Users(username=str(form.username.data),name=str(form.name.data), 
                         email=str(form.email.data),
                         favourite_color = str(form.favourite_color.data),
                         password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

        name=form.name.data
        form.name.data=''
        form.username.data=''
        form.favourite_color.data=''
        form.email.data=''
        form.password_hash.data=''
        flash('Thank you for the information')
    #     email=form.email.data
    our_users=Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# User Update
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name=request.form['name']
        name_to_update.email=request.form['email']
        name_to_update.favourite_color=request.form['favourite_color']
        name_to_update.username=request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash("Try again!")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id= id)
# Creating what the forms 
# creating a form class
class nameForm(FlaskForm):
    name=StringField("Please enter your name!",validators=[DataRequired()])
    submit=SubmitField("Enter")
class PasswordForm(FlaskForm):
    email=StringField("Please enter your email!",validators=[DataRequired()])
    password_hash=PasswordField("Please enter your password!",validators=[DataRequired()])
    submit=SubmitField("Enter")
# we can also provide html code through route
#Filterss!
# safe
# striptags
#title
#trim-> it used to remove trailing spaces(piche bache we spaces)
#capitalize
# lower
# upper
# passing a complete python dictionary
@app.route('/my')
def my():
    nosense="Hello,<strong>Listen</strong> to me"
    str1="making each letter capital is the use of title"
    favourite_books=["Atomic Habits","Harry Potter","DreamWorld",77]

    return render_template("my.html",stuff=nosense,str1=str1, favourite_books=favourite_books)

# creating a route -> decorator
@app.route('/')
#def index():
   # return "<h1>My first website using Flask!</h1>"
def index():
    my_name="Nitss"
    return render_template("index.html",first_name=my_name)
# localhost:5000/user/nitss
@app.route('/user/<name>')
#def user(name):
 #   return "<h1>Hello {}</h1>".format(name)
def user(name):
    return render_template("user.html",user_name=name)
# creating our own errors(custom errors)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500
@app.route('/name', methods=['GET','POST'])
def name():
    name=None
    form=nameForm()
    # validate
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash('Submitted Succesfully!')
    return render_template('name.html',
                            name=name,
                            form=form)
@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
    email=None
    password=None
    pw_to_check=None
    passed=None
    form=PasswordForm()
    # validate
    if form.validate_on_submit():
        email=form.email.data
        password=form.password_hash.data
        form.email.data=''
        form.password_hash.data=''
        # look up user by email
        pw_to_check=Users.query.filter_by(email=email).first()
        # check hashed password
        passed=check_password_hash(pw_to_check.password_hash,password)
        # flash('Submitted Succesfully!')
    return render_template('test_pw.html',
                            email=email,
                            password=password,
                            pw_to_check=pw_to_check,
                            passed=passed,
                            form=form)