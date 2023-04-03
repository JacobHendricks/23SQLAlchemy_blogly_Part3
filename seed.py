"""Seed file to make sample data for users db."""

from models import User, Post, db
from app import *

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add user
callahan = User(first_name='Callahan', last_name="Cowley",
                image_url="https://images.app.goo.gl/4iqKfJVskyGb4Pps7")
courtney = User(first_name='Courtney', last_name="Cowley")
bri = User(first_name='Bri', last_name="Hendricks",
           image_url="https://images.pexels.com/photos/384555/pexels-photo-384555.jpeg")
p1 = Post(title='First Post', content='Oh, hi.', user_id=1)
p2 = Post(title='Second Post', content='Oh, no.', user_id=2)
p3 = Post(title='Third Post', content='Wowsaaz', user_id=3)


# Add new objects to session, so they'll persist
db.session.add(callahan)
db.session.add(courtney)
db.session.add(bri)
db.session.commit()

db.session.add(p1)
db.session.add(p2)

# Commit--otherwise, this never gets saved!
db.session.commit()
