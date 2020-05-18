import sys
from datetime import datetime
from flask import render_template, request, flash, url_for, redirect
from app import app, db
from forms import VenueForm
from mock_data import (
    search_venues_data,
    edit_venue_data,
)
from venue.models import Venue, VENUE_SIMPLE_ATTRS
from show.models import Show, show_to_dict
from fixed_data import genres_from_ids


def get_venues_data():
    today = datetime.now()

    start_time_query = (
        db.session.query(Show.id, Show.venue_id)
        .filter(Show.start_time >= today)
        .subquery()
    )

    venues_query = (
        db.session.query(
            Venue.id,
            Venue.name,
            Venue.city,
            Venue.state,
            db.func.count(start_time_query.c.id),
        )
        .outerjoin(start_time_query, start_time_query.c.venue_id == Venue.id)
        .group_by(Venue.id)
    )

    venues = venues_query.all()

    cities_map = {}

    for venue in venues:
        city = venue[2]
        state, city_data = cities_map.get(city, [venue[3], []])
        city_data.append(
            {"id": venue[0], "name": venue[1], "num_upcoming_shows": venue[4]}
        )
        cities_map[city] = [state, city_data]

    return [
        {"city": city, "state": data[0], "venues": data[1]}
        for city, data in cities_map.items()
    ]


def get_show_venue_data(venue_id):
    today = datetime.now()
    venue = Venue.query.get(venue_id)
    shows = venue.shows
    past_shows = []
    upcoming_shows = []

    for show in shows:
        start_time = show.start_time
        show_data = show_to_dict(show)

        past_shows.append(show_data) if start_time < today else upcoming_shows.append(
            show_data
        )

    venue.genres = genres_from_ids(venue.genres)

    [
        setattr(venue, attr, value)
        for attr, value in {
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }.items()
    ]

    return venue


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = get_venues_data()
    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.   # noqa E501
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"   # noqa E501
    return render_template(
        "pages/search_venues.html",
        results=search_venues_data,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = get_show_venue_data(venue_id)
    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm()
    name = form.name.data
    created = False
    if form.validate_on_submit():
        try:
            attrs = {attr: getattr(form, attr).data for attr in VENUE_SIMPLE_ATTRS}

            genres = ",".join(x for x in form.genres.data)
            new_venue = Venue(**attrs, genres=genres)
            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            created = True
            flash("Venue " + name + " was successfully listed!")

        except:
            print(sys.exc_info())
        finally:
            db.session.close()

        if created:
            return redirect(url_for("index"))

    # TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash("An error occurred. Venue " + name + " could not be listed.")
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.   # noqa E501

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that   # noqa E501
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=edit_venue_data)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))

    return render_template("pages/home.html")
