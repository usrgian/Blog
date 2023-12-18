
from flask import Flask, redirect, url_for, render_template, flash, request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms import LoginForm, RegisterForm, CreatePostForm, AccountForm
import os
from db import create_db, db
from models import User, Post, Comment
import secrets
from PIL import Image
from flask_bcrypt import Bcrypt ##to improve security

bcrypt = Bcrypt()
login_manager = LoginManager()
DB_NAME = 'database.db' 


app = Flask(__name__)
app.secret_key = 'hshshsh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DB_NAME 
bcrypt.init_app(app) ##to initialize the bcrypt
login_manager.init_app(app) ##to initialize the login manager
login_manager.login_view = 'login'  ##endpoint for the login page
create_db(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/create-comment/<post_id>', methods=['POST'])
@login_required ##means only logged in users can access this
def create_comment(post_id):
    comment = request.form.get('comment')
    post = Post.query.get_or_404(post_id)
    if post:
        new_comment = Comment(comment=comment, user_pk=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/comment/<comment_pk>/delete')
@login_required ##means only logged in users can access this
def comment_delete(comment_pk):
    comment_del = Comment.query.get_or_404(comment_pk)
    db.session.delete(comment_del)
    db.session.commit()
    return redirect('/home')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) 

    return picture_fn 

@app.route('/', methods=['POST', 'GET']) ##url with methods
@app.route('/login', methods=['POST', 'GET']) ##url with methods
def login(): ##login func
    form = LoginForm()
    if request.method == 'POST': ##to post the data to the back-end
        email = form.email.data ##gets from the class LoginForm()
        password = form.password.data ##gets from the class LoginForm()
        user = User.query.filter_by(email=email).first() ##checks if email exists 
        if user:
            if bcrypt.check_password_hash(user.password, password): ##checks if the password is correct
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully', 'success') ##if user.password is correct
                return redirect(url_for('home')) ##redirect to the home page
            else:
                flash('Incorrect password', 'error') ##if user.password is incorrect
        else:
            flash('Email does not exist', 'error') ##if user.email does not exist

    return render_template('login.html', form=form) 


@app.route('/register', methods=['POST', 'GET']) ##url with methods
def register(): ##register func
    form = RegisterForm() 
    if request.method == 'POST': ##post the data to the back-end
        username = form.username.data  ##gets from the class RegisterForm()
        email = form.email.data ##gets from the class RegisterForm()
        password = form.password.data ##gets from the class RegisterForm()
        confirm_password = form.confirm_password.data ##gets from the class RegisterFrom()
        about_user = form.about_me.data  ##gets from the class RegisterForm()
        user = User.query.filter_by(email=email).first() ##checks if email exists 
        if user: 
            flash('Email already exist', 'error') ##if user.email already exists
        if password != confirm_password: ##checks if the passwords are the same
            flash('Passwords do not match', 'error') ##if passwords do not match
        else:
            new_user = User(username=username, email=email, about_user=about_user, password=bcrypt.generate_password_hash(password))
            db.session.add(new_user) ##add to the database
            db.session.commit() ##commit changes 
            flash('Account registered', 'success') 
            login_user(new_user) ##login as new user
            return redirect(url_for('home')) ##redirect to the home 
    return render_template('register.html', form=form) 

@app.route("/account", methods=['GET', 'POST']) ##url with methods
@login_required ##means only logged in users can access this
def account():
    form = AccountForm()
    if request.method == 'POST':
        if form.picture.data: 
            picture_file = save_picture(form.picture.data) ##gets from module form.py
            current_user.image_file = picture_file ##gets from module form.py
        current_user.username = form.username.data ##gets from module form.py
        current_user.email = form.email.data ##gets from module form.py
        current_user.about_user = form.about_me.data ##gets from module form.p
        db.session.commit() ##commit changes 
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_user
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@app.route('/search', methods=['POST'])
@login_required ##means logged in users can access this
def search():
    post = Post.query
    if request.method == 'POST':
        search = request.form.get('search') ##gets from the HTML form
        if search:
            posts = post.filter(Post.title.like('%' + search + '%'))
        return render_template('search.html', posts=posts)

@app.route('/create-post', methods=['POST','GET'])
@login_required ##means logged in users can access this
def create_post():
    form = CreatePostForm()
    if request.method == 'POST':
        title = form.title.data ##gets from wtforms module form.py
        content = form.content.data ##gets from wtforms module form.py
        user_pk = current_user.id
        new_post = Post(title=title, content=content, user_pk=user_pk)
        db.session.add(new_post) ##add new post to database
        db.session.commit() ##commit changes
        flash('Post created','success')
        return redirect('/home')
    return render_template('create_post.html', form=form)

@app.route('/poster/<user_id>')
@login_required ##means only logged in users can access this
def poster(user_id):
    poster = Post.query.get_or_404(user_id)
    return render_template('poster.html', poster=poster)
    
    
@app.route('/update/<post_pk>/post', methods=['POST','GET'])
@login_required ##means only logged in users can access this
def update_post(post_pk):
    post = Post.query.get_or_404(post_pk)
    form = CreatePostForm()
    if request.method == 'POST':
        post.title = form.title.data 
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been edited!",'success')
        return redirect('/home')
    elif request.method == 'GET':
        form.title.data =  post.title
        form.content.data =  post.content
    return render_template('create_post.html', form=form)

@app.route('/delete/<post_pk>/post') 
@login_required ##means only logged in users can access this
def delete_post(post_pk): 
    post = Post.query.get_or_404(post_pk)
    db.session.delete(post) ##delete post from database
    db.session.commit() ##commit changes
    flash('Post deleted','success')
    return redirect('/home')


@app.route('/posts/<post_pk>')
@login_required ##means only logged in users can access this
def posts(post_pk):
    post = Post.query.get_or_404(post_pk)
    return render_template('post.html', post=post)

@app.route('/logout')
@login_required ##means logged in users can access this
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/home')
@login_required ##means logged in users can access this
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)



if __name__=='__main__':
    app.run(debug=True)