from app import app
from flask import render_template
from flask_login import current_user
from .models import User

@app.route('/')
def homePage():
    users = User.query.all()


    following_set = set()
    if current_user.is_authenticated:    
        who_i_am_following = current_user.followed.all()
        print(who_i_am_following)
        for u in who_i_am_following:
            following_set.add(u.id)
        
        for u in users:
            if u.id in following_set:
                u.flag = True
            


    return render_template('index.html', users=users)


