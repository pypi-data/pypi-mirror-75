import unittest
from typing import Tuple, Dict, Optional, Any
from dataclasses import dataclass

from libbiomedit.lib import deserialize


class TestDeserialize(unittest.TestCase):
    def test_deserialize(self):
        @dataclass
        class Y:
            x: int
            y: Tuple[bool, bool]

        @dataclass
        class X:
            a: int
            pack: Y

        data = {"a": 1, "pack": {"x": 1, "y": [True, False]}}
        x = deserialize.deserialize(X)(data)

        self.assertEqual(x, X(a=1, pack=Y(x=1, y=(True, False))))

        with self.assertRaises(ValueError):
            deserialize.deserialize(Y)({"x": 1, "y": [True]})
        # typing.Dict
        @dataclass
        class Z:
            a: int
            dct: Dict[int, str]

        data = {"a": 1, "dct": {1: "x", 2: "y"}}
        z = deserialize.deserialize(Z)(data)

        self.assertEqual(z, Z(a=1, dct=data["dct"]))

        # typing.Optional
        self.assertEqual(deserialize.deserialize(
            Optional[int])(None), None)
        self.assertEqual(deserialize.deserialize(
            Optional[int])(1), 1)
        self.assertEqual(deserialize.deserialize(
            Any)(1), 1)
        self.assertEqual(deserialize.deserialize(
            Any)("1"), "1")

    def test_deserialize_tuple(self):
        with self.assertRaises(ValueError):
            deserialize.deserialize(Tuple[bool, bool])([True])
        self.assertEqual(
            deserialize.deserialize(Tuple[bool, bool])([True, False]),
            (True, False))
        self.assertEqual(
            deserialize.deserialize(Tuple[bool, ...])([True, False]),
            (True, False))
        self.assertEqual(
            deserialize.deserialize(Tuple[bool, ...])([True]),
            (True,))
