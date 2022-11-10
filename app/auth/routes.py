from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .forms import LoginForm, UserCreationForm
from app.models import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            u1 = User.query.filter_by(username=username).first()
            u2 = User.query.filter_by(email=email).first()
            if u1 and u2:
                flash('That username AND email already belong to an acount.', 'danger')
            elif u1:       
                flash('That username already belongs to an acoount', 'danger')
            elif u2:
                flash('That email already belongs to an acoount', 'danger')
            else:

                #add user to database
                user = User(username, email, password)
                
                #add instance to SQL
                user.saveToDB()
                flash('Successfully created a user', 'success')
                return redirect(url_for('auth.logMeIn'))   
    return render_template('signup.html', x=form)

@auth.route('/login', methods=["GET", "POST"])
def logMeIn():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash(f'Succesfully logged in. Welcome back, {user.username}!', 'success')
                    login_user(user)
                    return redirect(url_for('homePage'))
                else:
                    flash('Incorrect password.', 'danger')

            else:
                flash('A user with that username does not exist.', 'danger')



    return render_template('login.html', form=form)

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))


##############  API ROUTES ################
@auth.route('/api/signup', methods=["POST"])
def signMeUpAPI():
            data = request.json
            username = data['username']
            email = data['email']
            password = data['password']
            u1 = User.query.filter_by(username=username).first()
            u2 = User.query.filter_by(email=email).first()
            if u1 and u2:
                return {
                    'status': 'not ok',
                    'message': 'That username AND email already belong to an acount.'
                    }
            elif u1:
                return {
                    'status': 'not ok',
                    'message': 'That username already belongs to an acoount'
                    }  
            elif u2:
                return {
                    'status': 'not ok',
                    'message': 'That email already belongs to an acoount'
                    }
            else:

                #add user to database
                user = User(username, email, password)
                
                #add instance to SQL
                user.saveToDB()
                return {
                    'status': 'ok',
                    'message': 'Successfully created a user',
                }
               
@auth.route('/api/login', methods=["POST"])
def logMeInAPI():
    data = request.json
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': f'Succesfully logged in. Welcome back, {user.username}!',
                'user': user.to_dict()
            }
            
            login_user(user)
            return redirect(url_for('homePage'))
        else:
            return {
            'status': 'not ok',
            'message': 'Incorrect password.'
        }

    else:
        return {
            'status': 'not ok',
            'message': 'A user with that username does not exist.'
        }


from ..apiauthhelper import basic_auth
@auth.route('/api/token', methods=["POST"])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': f'Succesfully logged in. Welcome back, {user.username}!',
                'user': user.to_dict()
            }