from app import db


class AvailableTime(db.Model):
    __tablename__ = "available_time"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)

    # represents datetime.date.isoweekday: Monday = 1, Sunday = 7
    day_of_week = db.Column(db.Integer(), nullable=False)

    from_time = db.Column(db.Time(), nullable=False)
    to_time = db.Column(db.Time())
