from app import db
from models.card import Card
from models.condition import Condition
from models.printing import Printing


class Sku(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    card_id = db.Column(db.BIGINT, db.ForeignKey('card.id'), nullable=False)
    card = db.relationship(Card.__name__, backref=db.backref('skus', lazy=True))
    printing_id = db.Column(db.BIGINT, db.ForeignKey('printing.id'), nullable=False)
    printing = db.relationship(Printing.__name__)
    condition_id = db.Column(db.BIGINT, db.ForeignKey('condition.id'), nullable=False)
    condition = db.relationship(Condition.__name__)
    lowest_listing_price = db.Column(db.DECIMAL)
    lowest_base_price = db.Column(db.DECIMAL)
    lowest_shipping_price = db.Column(db.DECIMAL)
    market_price = db.Column(db.DECIMAL)
