from app import app
from flask import render_template


@app.route('/')
def homePage():
    people = [
        {
        'name': "Shoha",
        'age': 9000
    },
    {'name': "Brandt",
        'age': 9001}
        ,
        {'name': "Blair",
        'age': 8999}
        ]


    return render_template('index.html', names=people)


