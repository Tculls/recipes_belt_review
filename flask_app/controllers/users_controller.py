from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user_model import User
from flask_app.models.recipes_model import Recipe

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    print(session['user_id'])
    recipes = Recipe.get_all()
    logged_in_user = User.get_by_id({'id':session['user_id']})
    return render_template('dashboard.html', user = logged_in_user, recipes = recipes)

@app.route('/user/login', methods=['POST'])
def user_login():
    if not User.login(request.form):
        return redirect('/')
    return redirect('/')

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect ('/')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.is_valid_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        **request.form,
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def is_valid_login():

    user_in_db = User.get_by_email(request.form) 
    if not user_in_db:
        flash("Invalid Email or Password", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email or Password", 'login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")




