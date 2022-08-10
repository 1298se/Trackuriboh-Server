from app import db


class Condition(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255))
    abbreviation = db.Column(db.String(255))
    order = db.Column(db.INT)
