import unittest
from datetime import datetime, timezone, timedelta

from libbiomedit import metadata


class TestMetadata(unittest.TestCase):
    def test_new_str_type(self):
        def check(x, y):
            def _c(s):
                if not x < s < y:
                    raise ValueError("wrong")
                return s
            return _c

        T = metadata.new_str_type(check)
        t1 = T("1", "3")
        t2 = T("1", "3")
        self.assertIs(t1, t2)
        self.assertEqual(t1("2"), "2")
        with self.assertRaises(ValueError):
            t1("3")

    def setUp(self):
        self.dct = {
            "projectID": "Demo",
            "sender": "A"*32,
            "recipients": ["B"*256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*64,
            "checksum_algorithm": "SHA256",
            "compression_algorithm": "gzip",
            "version": "0.6"
        }
        self.metadata = metadata.MetaData(
            projectID="Demo",
            sender="A"*32,
            recipients=["B"*256],
            timestamp=datetime(2019, 10, 11, 14, 50, 12, 0,
                               timezone(timedelta(0, 3600), 'CET')),
            checksum="A"*64)

    def test_from_dict(self):
        self.assertEqual(
            metadata.MetaData.from_dict(self.dct),
            self.metadata)
        invalid_dicts = [{
            "projectID": "Demo",
            "sender": "A"*31,
            "recipients": ["B"*256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*64,
            "version": "0.6"
        }, {
            "projectID": "Demo",
            "sender": "A"*32,
            "recipients": ["B"*257],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*64,
            "version": "0.6"
        }, {
            "sender": "A"*32,
            "recipients": ["B"*256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*64,
            "version": "0.6"
        }, {
            "projectID": "Demo",
            "sender": "A"*32,
            "recipients": ["B"*256],
            "timestamp": "invalid timestamp",
            "checksum": "A"*64,
            "version": "0.6"
        }, {
            "projectID": "Demo",
            "sender": "A"*32,
            "recipients": ["B"*256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*65,
            "version": "0.6"
        }]
        for n, dct in enumerate(invalid_dicts):
            with self.subTest(index=n):
                with self.assertRaises(ValueError):
                    metadata.MetaData.from_dict(dct)
        dct = {
            "invalid_key": "Demo",
            "projectID": "Demo",
            "sender": "A"*32,
            "recipients": ["B"*256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A"*64,
            "version": "0.6"
        }
        with self.assertWarns(UserWarning):
            metadata.MetaData.from_dict(dct)

    def test_asdict(self):
        self.assertEqual(
            metadata.MetaData.asdict(self.metadata),
            self.dct)
