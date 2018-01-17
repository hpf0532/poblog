from flask import render_template, flash, redirect, request, url_for, g
from app import app, db
from app import login_manager
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, EditForm, PostForm
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime
from config import POSTS_PER_PAGE

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template("index.html",
                           title='Home',
                           posts=posts)

@app.route('/editblog', methods = ['GET', 'POST'])
@login_required
def editblog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, timestamp=datetime.now(), user_id=g.user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template("blog_edit.html",
                           form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user.is_anonymous() is not True:
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user.is_anonymous() is not True:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User' + username + 'not found.')
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'},
    ]
    return render_template('user.html',
                           user = user,
                           posts = posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.username)
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username = g.user.username))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)