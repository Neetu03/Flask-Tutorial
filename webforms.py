from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField,PasswordField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired, EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
# create Search form
class SearchForm(FlaskForm):
    searched=StringField("Searched",validators=[DataRequired()])
    submit=SubmitField("Submit")

# create login form
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Submit")


# create a Post form
class PostForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    # content=StringField("Content",validators=[DataRequired()],widget=TextArea())
    content=CKEditorField("Content",validators=[DataRequired()])
    author=StringField("Author")
    slug=StringField("Slug",validators=[DataRequired()])
    submit=SubmitField("Submit")

# creating user form
class UserForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    username=StringField("Username", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    favourite_color=StringField("Favourite Colour")
    about_author=TextAreaField("About")
    password_hash=PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2','Password must match!')])
    password_hash2=PasswordField('Confirm Password',validators=[DataRequired()])
    profile_pic=FileField("Profile Picture")
    submit=SubmitField("Submit")

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