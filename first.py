from flask import Flask, render_template

# creating a flask instance
app = Flask(__name__)

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

