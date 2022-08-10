from tcgplayer_request_handler import TCGPlayerRequestHandler


class DatabaseSyncWorker:
    def __init__(self, request_handler: TCGPlayerRequestHandler):
        self.request_handler = request_handler

    def update_card_database(self):
        pass
