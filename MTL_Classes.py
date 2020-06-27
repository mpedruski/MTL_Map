class Location:

    def __init__(self, name, long, lat, quartier, story, year, month):
        self.name = name
        self.long = long
        self.lat = lat
        self.quartier = quartier
        self.story = story
        self.year = year
        self.month = month

    def output(self):
        print("")
        print("{}".format(self.name))
        print("")
        print("-{}-".format(self.year))
        print("")
        print("{}".format(self.story))
