"""

Types class

Used for defining types

The supported ones should be:
- XML
- JSON

"""

from utils import constants


class Types:

    TYPE = None

    def __init__(self, type=constants.JSON):
        try:
            assert type == constants.XML or type == constants.JSON
            self.TYPE = type
        except TypeError:
            print("Type not supported")

    def get_type(self):
        return str(self.TYPE)

    def change_type(self, new_type=constants.JSON):
        self.TYPE = new_type
