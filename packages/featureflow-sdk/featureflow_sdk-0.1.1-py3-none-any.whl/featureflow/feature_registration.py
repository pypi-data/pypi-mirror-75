class FeatureRegistration:
    def __init__(self, key, failoverVariant, variants=[]):
        """docstring for __init__"""
        self.key = key
        self.failoverVariant = failoverVariant
        self.variants = [v.toJSON() for v in variants]

    def toJSON(self):
        """docstring for toJSON"""
        self.__dict__


class Variant:
    def __init__(self, key, name):
        """docstring for __init__"""
        self.key = key
        self.name = name

    def toJSON(self):
        """docstring for toJSON"""
        self.__dict__
