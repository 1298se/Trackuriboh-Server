from app import db


class Printing(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255))
    order = db.Column(db.INT)

    @staticmethod
    def from_tcgplayer_response(response: dict):
        return Printing(
            id=response['printingId'],
            name=response['name'],
            order=response['displayOrder'],
        )
