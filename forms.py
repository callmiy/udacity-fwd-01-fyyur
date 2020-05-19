from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    FieldList,
    FormField,
    Form,
)
from wtforms.validators import DataRequired, URL, Optional
from wtforms.widgets import TextArea
from fixed_data import states, GENRES
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_components import TimeField


def make_related_artist_field():
    QuerySelectField(
        "Select artist",
        validators=(DataRequired(),),
        query_factory=get_artists,
        allow_blank=True,
    )


def get_artists():
    from artist.models import Artist

    return Artist.query.all()


def get_venues():
    from venue.models import Venue

    return Venue.query.all()


def make_state_form_attrs():
    choices = [(state, state) for state in states]

    return {
        "label": "States",
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
        "Select artist",
        validators=(DataRequired(),),
        query_factory=get_artists,
        allow_blank=True,
    )
    venue = QuerySelectField(
        "Select venue",
        validators=(DataRequired(),),
        query_factory=get_venues,
        allow_blank=True,
    )
    start_time = DateTimeField(
        "Start time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = SelectField(**make_state_form_attrs())
    address = StringField("Address", validators=[DataRequired()])
    phone = StringField("Phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        **make_genre_form_attrs()
    )
    facebook_link = StringField("Facebook link", validators=[URL()])
    website = StringField("Website", validators=(Optional(), URL()))
    seeking_talent = BooleanField("Seeking talent")
    seeking_description = StringField("Seeking Description", widget=TextArea())


class AvailableTimeForm(Form):
    artist = make_related_artist_field()
    day_of_week = SelectField(
        "Day of week",
        validators=(DataRequired(),),
        choices=(
            ("", "-Select day-",),
            ("1", "Monday",),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
            ("7", "Sunday"),
        ),
    )
    from_time = TimeField("From time", validators=[DataRequired()])
    to_time = TimeField("To time", validators=(Optional(),))


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
    available_times = FieldList(
        FormField(AvailableTimeForm), min_entries=1, validators=(Optional(),)
    )


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
