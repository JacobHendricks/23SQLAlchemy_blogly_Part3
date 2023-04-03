
import datetime
from flask_sqlalchemy import SQLAlchemy

"""SQLAlchemy models for blogly."""


db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id={u.id} First Name={u.first_name} Last Name={u.last_name} URL={u.image_url}>"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='posttags', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Post Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class PostTag(db.Model):
    """Join table for Post and Tag"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
