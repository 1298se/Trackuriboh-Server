from app import db
from models.rarity import Rarity
from models.set import Set


class Card(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    # Blue-Eyes White Dragon
    name = db.Column(db.String(255), index=True)
    # name but no hyphens, semicolons, etc
    clean_name = db.Column(db.String(255), index=True)
    image_url = db.Column(db.Text)
    set_id = db.Column(db.BIGINT, db.ForeignKey('set.id'), nullable=False)
    set = db.relationship(Set.__name__, backref=db.backref('cards', lazy=True))
    number = db.Column(db.String(255), index=True)
    # Ultra rare
    rarity_id = db.Column(db.BIGINT, db.ForeignKey('rarity.id'), nullable=False)
    rarity = db.relationship(Rarity.__name__)
    # LIGHT
    attribute = db.Column(db.String(255))
    # Normal Monster
    card_type = db.Column(db.String(255))
    attack = db.Column(db.String(255))
    defense = db.Column(db.String(255))
    description = db.Column(db.Text)