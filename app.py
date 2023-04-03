"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "ihaveasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()


@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


##############################################################################
# User route


@app.route('/users')
def users_page():
    """Shows page with all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/users.html', users=users)


@app.route('/users/new')
def user_form():
    """New user form"""
    return render_template('users/add.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Submit form to add user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name,
                    image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show details about single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template('users/details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Show edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Submit form to edit user data"""
    user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} deleted.")

    return redirect('/users')

##############################################################################
# Posts route


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """New post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form_submit(user_id):
    """Submit form to add new post"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form["title"],
                    content=request.form["content"],
                    user_id=user.id,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def post(post_id):
    """Show details about single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit details about single post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def Submit_edit(post_id):
    """Handle form submission for updating a single post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete single post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


##############################################################################
# Tags route

@app.route('/tags')
def tags_page():
    """List all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """Show details about a tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/new')
def tag_form():
    """Show form to add new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Submit form to add tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' created.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_edit_tag(tag_id):
    """Submit form to edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name} deleted.")

    return redirect('/tags')
