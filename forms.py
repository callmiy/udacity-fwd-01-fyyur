from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL
from fixed_data import states, genres


def make_state_form_attrs():
    choices = ((state, state) for state in states)

    return {
        "label": "states",
        "choices": choices,
        "validators": (
            DataRequired(),
            AnyOf(values=states, message="Please select from dropdown"),
        ),
    }


def make_genre_form_attrs():
    return {
        "label": "genres",
        "choices": genres.items(),
        "validators": (DataRequired(),),
    }


class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
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


class ArtistForm(Form):
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
        validators=[URL()],
    )


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
