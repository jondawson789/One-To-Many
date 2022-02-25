"""Blogly application."""

from models import db, connect_db, User, Post, Tag
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    return redirect('/Users')

@app.route('/Users')
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new', methods = ["GET"])
def return_user_form():
    return render_template("users-new.html")

@app.route('/users/new', methods = ["POST"])
def add_user():

    new_user = User(first_name = request.form["first_name"], last_name = request.form["last_name"], img_url = request.form["img_url"])
    db.session.add(new_user)
    db.session.commit()

    return redirect('/Users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)
    return render_template("user-detail.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    
    return render_template('user-edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']
    
    db.session.add(user)
    db.session.commit()

    return redirect('/Users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/Users")

#--------------------------------------------------------------------

@app.route('/users/<int:user_id>/posts/new', methods = ["GET"])
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def submit_post(user_id):

    new_post = Post(title = request.form["post_title"], content = request.form["post_content"], user_id = user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template("show-post.html", post=post)

@app.route('/post/<int:post_id>/edit', methods=["GET"])
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('post-edit.html', post=post)

@app.route('/post/<int:post_id>/edit', methods = ["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["post_title"]
    post.content = request.form["post_content"]
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/post/{post_id}")

@app.route('/post/<int:post_id>/delete', methods=["POST"])
def post_destroy(post_id):

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/Users")

#--------------------------------------------------------------------------------------
@app.route('/tags')
def list_tags()
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

#@app.route('/tags/<int:tag_id>')