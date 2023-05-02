"""Blogly application."""

from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

db.create_all()

@app.route('/')
def go_home():
    return redirect("/users")


@app.route("/users", methods=["GET"])
def list_users():
    """List pets and show add form."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("homelist.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_form():
    return render_template("newform.html")

@app.route("/users/new", methods=["POST"])
def add():
    first = request.form['fn']
    last = request.form['ln']
    url = request.form['url']

    user = User(first_name=first, last_name=last, image_url=url)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    post = Post.query.filter(Post.user_id == user_id)

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user, post=post)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fn']
    user.last_name = request.form['ln']
    user.image_url = request.form['url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def load_post_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("postadd.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_new_post(user_id):
    user = User.query.get_or_404(user_id)
    t = request.form['tt']
    c = request.form['cc']
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")

    post = Post(date=dt, title=t, content=c, u=user)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user.id}")
    
@app.route("/posts/<int:post_id>")
def handle_load_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("postdetail.html", post=post)



@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def handle_edit_load(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("postedit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods={"POST"})
def handle_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['tt']
    post.content = request.form['ct']

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/tags", methods=["GET"])
def load_tags_page():

    tag = Tag.query.all()

    return render_template("tags.html", tag=tag)

@app.route("/tags/new", methods=["GET"])
def new_tag():
    
    return render_template("newtag.html")

@app.route("/tags/new", methods=["POST"])
def handle_new_tag():
    
    name = request.form['tn']

    t = Tag(name=name)

    db.session.add(t)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>", methods=["GET"])
def load_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tagsdetail.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["GET"])
def edit_tag_load(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tagsedit.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_finish(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tn']

    
    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag.id}")
#@app.route("/tags/<int:tag_id>/delete", methods=["GET"])