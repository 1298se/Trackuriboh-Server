from app import db


class Rarity(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255), primary_key=True, index=True)