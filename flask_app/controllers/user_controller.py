from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "uuid" in session:
        return redirect("/dashboard")
    return render_template("index.html")


@app.route('/register',methods=['POST'])
def register():

    if not User.register_validator(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['uuid'] = id
    # ['user_id'] user_id just a var you make , make sure to use the same var name 
    return redirect('/dashboard')







@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect("/")

    user = User.get_by_email({"email": request.form['email']})
    session['uuid'] = user.id
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if 'uuid' not in session:
        return redirect('/logout')
    data ={
        'id': session['uuid']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),recipes=Recipe.get_all())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")