class BursaWebpage:

    def __init__(self):
        pass

    @property
    def official(self):
        return "http://www.bursamalaysia.com"

    @property
    def equities(self):
        return "%s/market/securities/equities" % self.official

    @property
    def indices(self):
        return "%s/indices" % self.equities

    @property
    def pn17_and_gn3_companies(self):
        return "%s/pn17-and-gn3-companies/" % self.list_of_companies

    @property
    def listed_companies(self):
        return "%s/market/listed-companies" % self.official

    @property
    def list_of_companies(self):
        return "%s/list-of-companies" % self.listed_companies
    
    @property
    def ace_market(self):
        return "%s/ace-market/" % self.list_of_companies

    @property
    def leap_market(self):
        return "%s/leap-market/" % self.list_of_companies

    @property
    def main_market(self):
        return "%s/main-market/" % self.list_of_companies


if __name__ == "__main__":
    pass
