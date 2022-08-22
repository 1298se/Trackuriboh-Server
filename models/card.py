from app import db


class Card(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    # Blue-Eyes White Dragon
    name = db.Column(db.String(255), index=True)
    # name but without hyphens, semicolons, etc
    clean_name = db.Column(db.String(255), index=True)
    image_url = db.Column(db.Text)
    set_id = db.Column(db.BIGINT, db.ForeignKey("set.id"), nullable=False)
    set = db.relationship("Set", back_populates="cards")
    number = db.Column(db.String(255), index=True)
    # Ultra rare
    rarity = db.Column(db.String(255))
    # LIGHT
    attribute = db.Column(db.String(255))
    # Normal Monster
    card_type = db.Column(db.String(255))
    # Dragon
    monster_type = db.Column(db.String(255))
    attack = db.Column(db.String(255))
    defense = db.Column(db.String(255))
    description = db.Column(db.Text)
    skus = db.relationship("Sku", back_populates="card")

    @staticmethod
    def parse_extended_data(extended_data: list[dict]) -> dict:
        return {data['name']: data['value'] for data in extended_data}

    @staticmethod
    def from_tcgplayer_response(response: dict):
        card_metadata = Card.parse_extended_data(response['extendedData'])

        return Card(
            id=response['productId'],
            name=response['name'],
            clean_name=response['cleanName'],
            image_url=response['imageUrl'],
            set_id=response['groupId'],
            number=card_metadata.get('Number'),
            rarity=card_metadata.get('Rarity'),
            attribute=card_metadata.get('Attribute'),
            card_type=card_metadata.get('Card Type'),
            monster_type=card_metadata.get('MonsterType'),
            attack=card_metadata.get('Attack'),
            defense=card_metadata.get('Defense'),
            description=card_metadata.get('Description'),
        )
