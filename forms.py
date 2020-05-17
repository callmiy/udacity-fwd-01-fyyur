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
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
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
