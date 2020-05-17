from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL


def make_state_form_attrs():
    states = (
        "",
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "DC",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    )

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
    genres = {
        "1": "Alternative",
        "2": "Blues",
        "3": "Classical",
        "4": "Country",
        "5": "Electronic",
        "6": "Folk",
        "7": "Funk",
        "8": "Hip-Hop",
        "9": "Heavy Metal",
        "10": "Instrumental",
        "11": "Jazz",
        "12": "Musical Theatre",
        "13": "Pop",
        "14": "Punk",
        "15": "R&B",
        "16": "Reggae",
        "17": "Rock n Roll",
        "18": "Soul",
        "19": "Other",
    }
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
