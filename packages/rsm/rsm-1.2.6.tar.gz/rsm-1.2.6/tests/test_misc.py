from unittest import TestCase
from rsm.utils import misc

d = {
    "firstName": "John",
    "lastName": "Doe",
    "age": "27",
    "hobby": ["Tennis", "Volleyball", "Foo"],
    "attrib": {
        "stamina": 80,
        "dexterity": 15,
        "intelligence": 9000,
        "wisdom": 50
    }
}


class TestMisc(TestCase):
    def test_flatten(self):
        flat = misc.dict_to_flat(d)
        print(flat)
        assert flat
