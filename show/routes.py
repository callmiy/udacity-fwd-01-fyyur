import sys
from flask import render_template, flash, redirect, url_for
from app import app
from forms import ShowForm
from show.models import Show, show_to_dict
from app import db


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    data = [show_to_dict(show) for show in shows]
    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    created = False

    if form.validate_on_submit():
        try:
            new_show = Show(start_time=form.start_time.data)
            new_show.venue = form.venue.data
            new_show.artist = form.artist.data
            db.session.add(new_show)
            db.session.commit()
            # on successful db insert, flash success
            created = True
            flash("Show was successfully listed!")

        except:
            print(sys.exc_info())
        finally:
            db.session.close()

        if created:
            return redirect(url_for("index"))

    # TODO: on unsuccessful db insert, flash an error instead.
    flash("An error occurred. Show could not be listed.")
    return render_template("forms/new_show.html", form=form)
