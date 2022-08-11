from extensions import db


class Rarity(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255), primary_key=True, index=True)

    @staticmethod
    def from_tcgplayer_response(response: dict):
        return Rarity(
            id=response['rarityId'],
            name=response['displayText'],
        )
