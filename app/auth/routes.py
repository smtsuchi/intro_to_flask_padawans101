from flask import Blueprint, render_template, request, redirect, url_for

from .forms import UserCreationForm
from app.models import User

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)


            

            #add user to database
            user = User(username, email, password)\
            
            #add instance to SQL
            user.saveToDB()

            return redirect(url_for('auth.logMeIn'))   
    return render_template('signup.html', x=form)

@auth.route('/login')
def logMeIn():





    return render_template('login.html')