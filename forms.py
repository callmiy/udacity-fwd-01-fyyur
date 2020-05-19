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
from wtforms.validators import DataRequired, URL, Optional, ValidationError
from wtforms.widgets import TextArea
from fixed_data import states, GENRES, DAYS_OF_WEEK
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


def artist_available_times_validator(form, field):
    artist = field.data
    available_times = artist.available_times

    if not len(available_times):
        return

    start_time_data = form.start_time.data
    start_date = start_time_data.date()
    start_time = start_time_data.time()
    selected_week_day = start_date.isoweekday()

    available = False

    for at in available_times:
        day_of_week = at.day_of_week
        from_time = at.from_time
        to_time = at.to_time
        not_week_day = day_of_week != selected_week_day
        earlier_than_available = start_time < from_time
        later_than_available = to_time and (to_time < start_time)

        if not_week_day or earlier_than_available or later_than_available:
            continue
        available = True
        break

    if not available:
        raise ValidationError("Artist is not available for booking on date")


class ShowForm(FlaskForm):
    artist = QuerySelectField(
        "Select artist",
        validators=(DataRequired(), artist_available_times_validator,),
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
        "Day of week", validators=(DataRequired(),), choices=DAYS_OF_WEEK.items(),
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
