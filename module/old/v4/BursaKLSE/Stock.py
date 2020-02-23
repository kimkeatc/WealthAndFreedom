class Stock:

    history = []

    def __init__(self):

        self.full_name = None
        self.short_name = None
        self.code = None

        self.market_type = None
        self.sector = None  # Segment of the economy
        self.industry = None  # Much specific group

        self.weblink = None
        self.klse_link = None
        self.bursa_link = None


class Utility:

    def __init__(self):
        pass

    @staticmethod
    def getMarkets():
        pass


if __name__ == '__main__':
    pass
