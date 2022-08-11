from extensions import db


class Set(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255), index=True)
    code = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
