from flask import render_template, flash, redirect, request, url_for, g
from app import app, db
from app import login_manager
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, current_user, logout_user


@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@app.route('/')
@app.route('/index')
@login_required
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
    if current_user.is_anonymous() is not True:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_anonymous() is not True:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)