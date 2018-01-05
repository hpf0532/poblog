from flask import render_template, flash, redirect, request, url_for
from app import app
from app import login_manager
from models import User
from forms import LoginForm
from flask_login import login_required, login_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'hpf'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        print user
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
#            return redirect(request.args.get('next') or url_for('index'))
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)