from app import db


class SkuPricingInfo(db.Model):
    date = db.Column(db.DateTime, primary_key=True)
    sku_id = db.Column(db.BIGINT, db.ForeignKey('sku.id'), primary_key=True, nullable=False)
    sku = db.relationship("Sku", back_populates="pricing_info")
    lowest_base_price = db.Column(db.FLOAT)
    lowest_shipping_price = db.Column(db.FLOAT)
    lowest_listing_price = db.Column(db.FLOAT)
    market_price = db.Column(db.FLOAT)

    @staticmethod
    def from_tcgplayer_response(response: dict, date):
        return SkuPricingInfo(
            date=date,
            sku_id=response['skuId'],
            lowest_base_price=response['lowPrice'],
            lowest_shipping_price=response['lowestShipping'],
            lowest_listing_price=response['lowestListingPrice'],
            market_price=response['marketPrice']
        )
