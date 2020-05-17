from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
)
from wtforms.validators import DataRequired, URL, Optional
from wtforms.widgets import TextArea
from fixed_data import states, GENRES
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def get_artists():
    from artist.models import Artist
    return Artist.query.all()


def make_state_form_attrs():
    choices = [(state, state) for state in states]

    return {
        "label": "states",
        "choices": choices,
        "validators": (DataRequired(),),
    }


def make_genre_form_attrs():
    return {
        "label": "genres",
        "choices": GENRES.items(),
        "validators": (DataRequired(),),
    }


class ShowForm(FlaskForm):
    artist = QuerySelectField(
        "Select artist", validators=(DataRequired(),), query_factory=get_artists
    )
    venue = StringField("Select venue", validators=(DataRequired(),))
    start_time = DateTimeField(
        "Start time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(**make_state_form_attrs())
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        **make_genre_form_attrs()
    )
    facebook_link = StringField("facebook_link", validators=[URL()])


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(**make_state_form_attrs())
    phone = StringField(
        # TODO implement validation logic for state
        "phone"
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        **make_genre_form_attrs()
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        "facebook_link",
        validators=(Optional(), URL()),
    )
    website = StringField("Website", validators=(Optional(), URL()))
    seeking_venue = BooleanField("Seeking Venue")
    seeking_description = StringField("Seeking Description", widget=TextArea())


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
