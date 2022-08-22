from app import db
from models.sku_pricing_info import SkuPricingInfo


class Sku(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    card_id = db.Column(db.BIGINT, db.ForeignKey('card.id'), nullable=False)
    card = db.relationship("Card", back_populates="skus")
    printing_id = db.Column(db.BIGINT, db.ForeignKey('printing.id'))
    printing = db.relationship("Printing")
    condition_id = db.Column(db.BIGINT, db.ForeignKey('condition.id'))
    condition = db.relationship("Condition")
    current_lowest_base_price = db.Column(db.FLOAT)
    current_lowest_shipping_price = db.Column(db.FLOAT)
    current_lowest_listing_price = db.Column(db.FLOAT)
    current_market_price = db.Column(db.FLOAT)
    pricing_info = db.relationship("SkuPricingInfo", back_populates="sku")

    @staticmethod
    def from_tcgplayer_response(response: dict):
        return Sku(
            id=response['skuId'],
            card_id=response['productId'],
            printing_id=response['printingId'],
            condition_id=response.get('conditionId'),
        )
