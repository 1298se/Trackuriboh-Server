from datetime import datetime

from app import db


class Set(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255), index=True)
    code = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    cards = db.relationship("Card", back_populates="set")

    @staticmethod
    def from_tcgplayer_response(response: dict):
        return Set(
            id=response['groupId'],
            name=response['name'],
            code=response['abbreviation'],
            release_date=Set._parse_response_release_date(response['publishedOn']),
            modified_date=Set._parse_response_modified_date(response['modifiedOn']),
        )

    @staticmethod
    def _parse_response_release_date(date: str):
        # 2022-09-30T00:00:00
        # We take only the year-month-day
        date = date[0:10]
        return datetime.strptime(date, "%Y-%m-%d")

    @staticmethod
    def _parse_response_modified_date(date: str):
        # 2022-07-20T20:42:36.44
        # We only take up to including seconds
        date = date[0:19]
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
