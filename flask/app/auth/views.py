from flask import render_template,session,redirect,flash,url_for
from app.forms import LoginForm, SignupForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from app.firestore_service import get_user, user_put
from app.models  import UserData, UserModel


@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form' : login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        user_doc = get_user(username)
        print(user_doc is not None)
        if not user_doc.empty:
            password_from_db = user_doc['password'][0]
            name = user_doc['name'][0]
            fecha_nacimiento = user_doc['fecha_nacimiento'][0]
            correo_electronico = user_doc['correo_electronico'][0]
            print(password_from_db)
            if password == password_from_db or check_password_hash(user_doc['password'][0], password):
                user_data = UserData(username,password,name,fecha_nacimiento,correo_electronico)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('main'))
            else:
                flash('La informacion no coincide')
            
        else:
            flash('Usuario no existe')

        
        return redirect(url_for('index'))
    return render_template('login.html',**context)

@auth.route('signup',methods=['GET','POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form' : signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        name = signup_form.name.data
        fecha_nacimiento = signup_form.fecha_nacimiento.data
        correo_electronico = signup_form.correo_electronico.data

        user_doc = get_user(username)
        if user_doc.empty:
            password_hash = generate_password_hash(password)
            user_data = UserData(username,password_hash,name,fecha_nacimiento,correo_electronico)
            user_put(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenidos') 
            return redirect(url_for('main'))
        else:
            flash('el usuario ya existe')
        
    return render_template('signup.html',**context)



@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))
