class Location:

    def __init__(self, name, long, lat, quartier, story, year):
        self.name = name
        self.long = long
        self.lat = lat
        self.quartier = quartier
        self.story = story
        self.year = year

    def output(self):
        print("")
        print("{}".format(self.name))
        print("")
        print("-{}-".format(self.year))
        print("")
        print("{}".format(self.story))
