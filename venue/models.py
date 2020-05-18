from app import db

VENUE_SIMPLE_ATTRS = (
    "name",
    "city",
    "state",
    "address",
    "phone",
    "image_link",
    "facebook_link",
    "website",
    "seeking_talent",
    "seeking_description",
)


class Venue(db.Model):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String)
    genres = db.Column(db.String(120), nullable=False)

    shows = db.relationship("Show", lazy=True, backref=db.backref("venue", lazy=True),)

    def __repr__(self):
        return self.name

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
