import sys
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from artist.models import Artist, ARTIST_SIMPLE_ATTRS
from mock_data import (
    search_artists_data,
    edit_artist_data,
)
from forms import ArtistForm
from fixed_data import genres_from_ids


@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.   # noqa E501
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".   # noqa E501
    # search for "band" should return "The Wild Sax Band".
    return render_template(
        "pages/search_artists.html",
        results=search_artists_data,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = Artist.query.get(artist_id)
    data.genres = genres_from_ids(data.genres)
    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=edit_artist_data)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for("show_artist", artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm()
    name = form.name.data
    created = False

    if form.validate_on_submit():
        try:
            attrs = {attr: getattr(form, attr).data for attr in ARTIST_SIMPLE_ATTRS}

            genres = ",".join(x for x in form.genres.data)
            new_artist = Artist(**attrs, genres=genres)
            db.session.add(new_artist)
            db.session.commit()
            # on successful db insert, flash success
            created = True
            flash("Artist " + name + " was successfully listed!")

        except:
            print(sys.exc_info())
        finally:
            db.session.close()

        if created:
            return redirect(url_for("index"))

    # TODO: on unsuccessful db insert, flash an error instead.
    flash("An error occurred. Artist " + name + " could not be listed.")
    return render_template("forms/new_artist.html", form=form)
