import unittest
from unittest import mock
from typing import Optional
from contextlib import contextmanager

from libbiomedit import crypt
from libbiomedit.crypt import gpg

CN_UID = gpg.Uid(full_name="Chuck Norris",
                 email="chuck.norris@roundhouse.gov")
DCC_UID = gpg.Uid(full_name="DCC Test (Test key for transferprotocol)",
                  email="dcc@sib.swiss")


test_key_data = dict(
    key_id="AAAAAAAAAAAAAAAA",
    fingerprint="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    validity=gpg.Validity.ultimately_valid,
    key_length=4096,
    pub_key_algorithm=1,
    creation_date="1550241679",
    uids=(CN_UID,),
    owner_trust="u",
    key_type=gpg.KeyType.public,
    origin="http://keyserver.dcc.sib.swiss:11371",
    signatures=(
        gpg.Signature(issuer_uid=CN_UID, issuer_key_id="FDC66B7A5F6FFD4B",
                      creation_date="1550241679", signature_class="13x"),
        gpg.Signature(issuer_uid=DCC_UID, issuer_key_id="3A6500D5C1DE39AC",
                      creation_date="1571225229", signature_class="13x")
        ),
    key_capabilities=frozenset((gpg.KeyCapability.Sign(True),
                                gpg.KeyCapability.Sign(False),
                                gpg.KeyCapability.Certify(True),
                                gpg.KeyCapability.Certify(False),
                                gpg.KeyCapability.Encrypt(True))),
    sub_keys=(gpg.SubKey(
        key_type=gpg.KeyType.public,
        key_id="D892C41917B20115",
        fingerprint="55C5314BB9EFD19AE7CC4774D892C41917B20115",
        validity=gpg.Validity.ultimately_valid,
        key_length=4096,
        pub_key_algorithm=1,
        creation_date="1550241679",
        key_capabilities=frozenset((gpg.KeyCapability.Encrypt(False),))
        ),)
    )


def fake_key(**kwargs):
    return gpg.Key(**{**test_key_data, **kwargs})


class TestCrypt(unittest.TestCase):
    keyserver = "http://keyserver.dcc.sib.swiss"

    def setUp(self):
        self.key1 = fake_key()

    def test_assert_keyserver_origin_valid(self):
        keys = (self.key1, fake_key(origin="keyserver.dcc.sib.swiss"))
        for key in keys:
            for keyserver in ("http://keyserver.dcc.sib.swiss:11371",
                              "http://keyserver.dcc.sib.swiss",
                              "keyserver.dcc.sib.swiss:11371",
                              "hkp://keyserver.dcc.sib.swiss:11371",
                              "keyserver.dcc.sib.swiss"):
                with self.subTest(key=keys.index(key), keyserver=keyserver):
                    crypt.assert_keyserver_origin_valid(key,
                                                        keyserver=keyserver)
        with self.assertRaises(RuntimeError):
            crypt.assert_keyserver_origin_valid(self.key1,
                                                keyserver="fakekeyserver.dcc.sib.swiss")
        with self.assertRaises(RuntimeError):
            crypt.assert_keyserver_origin_valid(self.key1,
                                                keyserver="keyserver.dcc.sib.swiss:11111")

    def test_assert_key_is_signed(self):
        crypt.assert_key_is_signed(self.key1, sig_keyid="3A6500D5C1DE39AC")
        with self.assertRaises(RuntimeError):
            crypt.assert_key_is_signed(self.key1, sig_keyid="WRONG_ID")
        rev_sig = gpg.RevocationSignature(
            issuer_uid=DCC_UID, issuer_key_id="3A6500D5C1DE39AC",
            creation_date="1588066811", signature_class="30x",
            reason="00",
            comment="revsig\\nInvalid email")
        with self.assertRaises(RuntimeError):
            crypt.assert_key_is_signed(
                fake_key(signatures=(rev_sig,)),
                sig_keyid="3A6500D5C1DE39AC")

    def test_validate_pub_key(self):
        crypt.validate_pub_key(self.key1, validation_keyid="3A6500D5C1DE39AC",
                               keyserver_url="http://keyserver.dcc.sib.swiss:11371")
        with self.assertRaises(RuntimeError):
            crypt.validate_pub_key(fake_key(validity=gpg.Validity.revoked),
                                   validation_keyid="3A6500D5C1DE39AC",
                                   keyserver_url="http://keyserver.dcc.sib.swiss:11371")
        # All other cases are covered in the above assert_* tests

    def test_split_url(self):
        self.assertEqual(
            crypt.split_url("http://keyserver.dcc.sib.swiss:11371"),
            ("http://", "keyserver.dcc.sib.swiss", ":11371"))
        self.assertEqual(
            crypt.split_url("keyserver.dcc.sib.swiss:11371"),
            (None, "keyserver.dcc.sib.swiss", ":11371"))
        self.assertEqual(
            crypt.split_url("http://keyserver.dcc.sib.swiss"),
            ("http://", "keyserver.dcc.sib.swiss", None))
        self.assertEqual(
            crypt.split_url("keyserver.dcc.sib.swiss"),
            (None, "keyserver.dcc.sib.swiss", None))
        with self.assertRaises(RuntimeError):
            crypt.split_url("keyserver.dcc:sib.swiss")

    def test_verify_metadata_signature(self):
        class MockTar:
            """Mock for tar extract"""

            def __init__(self, *, metadata=None, signature=None):
                self.contents = {}
                if metadata:
                    self.contents[crypt.METADATA_FILE] = metadata
                if signature:
                    self.contents[crypt.METADATA_FILE_SIG] = signature
                self.signature = signature
                self.metadata = metadata

                self.should_pass = metadata is not None and signature == b"valid"

            def extractfile(self, f: str):
                _ = self.contents[f]
                mock_f = mock.Mock()
                mock_f.read = mock.Mock(return_value=self.signature)
                return mock_f

            def __repr__(self):
                return f"MockTarr({self.metadata}, {self.signature})"

        def mock_gpg_verify(_metadata, sig):
            if sig != b"valid":
                raise crypt.gpg.cmd.GPGError("Invalid")
            return "MOCK_FINGERPRINT"

        def mock_gpg_key_id(_metadata):
            return "MOCK_KEY_ID"

        for mock_tar in (MockTar(), MockTar(metadata=...),
                         MockTar(signature=b"valid"), MockTar(
                             signature=b"invalid"),
                         MockTar(metadata=..., signature=b"valid"),
                         MockTar(metadata=..., signature=b"invalid")):
            with self.subTest(tar=repr(mock_tar)):
                mock_tar_open_obj = mock.Mock(return_value=mock_tar)

                @contextmanager
                def mock_tar_open(f):
                    yield mock_tar_open_obj(f)  # pylint: disable=cell-var-from-loop

                mock_gpg_store = mock.Mock()
                mock_gpg_store.verify = mock_gpg_verify
                mock_validate_keys_iter = mock.MagicMock()
                mock_validate_keys = mock.Mock(
                    return_value=mock_validate_keys_iter)
                with mock.patch("tarfile.open", mock_tar_open), \
                        mock.patch("libbiomedit.crypt.validated_keys_by_ids",
                                   mock_validate_keys), \
                        mock.patch("libbiomedit.crypt.extract_key_id_from_sig",
                                   mock_gpg_key_id):
                    with assert_conditional_raise(self, None if mock_tar.should_pass
                                                  else (RuntimeError, crypt.gpg.cmd.GPGError)):
                        crypt.verify_metadata_signature(
                            "/faketar.tar", mock_gpg_store,
                            "ABCD",
                            "http://fakekeyserver.dcc.sib.swiss:11371")
                mock_tar_open_obj.assert_called_once_with("/faketar.tar")
                if mock_tar.should_pass:
                    mock_validate_keys.assert_called_once_with(
                        ("MOCK_KEY_ID",), mock_gpg_store, "ABCD",
                        "http://fakekeyserver.dcc.sib.swiss:11371",
                        url_opener=crypt.urllib.request.urlopen)
                    mock_validate_keys_iter.__next__.assert_called_once()

    def test_validated_keys_by_ids(self):
        key_A = self.key1
        key_B = fake_key(key_id=16*"B")
        key_C = fake_key(key_id=16*"C")
        key_D = fake_key(key_id=16*"D")

        class MockGPGStore:
            def __init__(self, keys, keyserver_keys):
                self.keys = [(key.key_id, key) for key in keys]
                self.keyserver_keys = [(key.key_id, key)
                                       for key in keyserver_keys]

            def list_pub_keys(self, keys, sigs):
                _ = sigs
                return [key for key_id, key in self.keys if key_id in keys]

            def recv_keys(self, *key_ids, keyserver=None, url_opener=None):
                _ = keyserver
                _ = url_opener
                self.keys += [(key_id, key) for key_id, key in self.keyserver_keys
                              if key_id in key_ids]

        for gpg_store in (
                MockGPGStore([key_A, key_B, key_C, key_D], []),
                MockGPGStore([key_A], [key_B, key_C]),
                MockGPGStore([], [key_A, key_B, key_C])):
            with self.subTest(store=[key_id for key_id, _key in gpg_store.keys]):
                available_keys = frozenset(
                    key_id for key_id, key in gpg_store.keys)
                should_refresh = [key for key in [
                    key_A, key_B] if key.key_id in available_keys]
                refresh_keys = mock.Mock(side_effect=lambda keys, **_: keys)
                validate_pub_key = mock.Mock()
                with mock.patch("libbiomedit.crypt.refresh_keys", refresh_keys),\
                        mock.patch("libbiomedit.crypt.validate_pub_key", validate_pub_key):
                    validated = crypt.validated_keys_by_ids(
                        (16*"A", 16*"B"), gpg_store, validation_keyid=..., keyserver_url=None)
                    self.assertEqual(list(validated), [key_A, key_B])
                refresh_keys.assert_called_once_with(
                    keys=should_refresh, gpg_store=gpg_store, sigs=True,
                    url_opener=crypt.urllib.request.urlopen, keyserver_url=None)
                # Calls to list_pub_keys and recv_keys are implicitely checked by
                # comparing the output of validated_keys_by_ids with the expected output
                validate_pub_key.assert_has_calls((
                    mock.call(key_A, ..., None),
                    mock.call(key_B, ..., None)),
                    any_order=True)

        with self.subTest(store="corrupted"):
            gpg_store = mock.Mock()
            gpg_store.list_pub_keys = mock.Mock(return_value=[key_A]*10)
            with self.assertRaises(RuntimeError):
                next(crypt.validated_keys_by_ids(
                    (16*"A", 16*"B"), gpg_store, validation_keyid=..., keyserver_url=None))

    def test_refresh_keys(self):
        keys = (self.key1,
                fake_key(fingerprint=40*"B", origin="keyserver2"),
                fake_key(fingerprint=40*"C", origin="keyserver2"),
                fake_key(fingerprint=40*"D", origin=None))

        def new_gpg_store(refreshed_keys):
            gpg_store = mock.Mock()
            gpg_store.recv_keys = mock.Mock()
            gpg_store.list_pub_keys = mock.Mock(return_value=refreshed_keys)
            return gpg_store

        # Check that when no keyserver is specified, only keys with an
        # origin are attempted to be refreshed.
        gpg_store = new_gpg_store(keys)
        urlopen = crypt.urllib.request.urlopen
        new_keys = crypt.refresh_keys(keys, gpg_store, sigs=...,
                                      keyserver_url=None, url_opener=urlopen)
        # keys must be the same before and after the refresh.
        self.assertEqual(keys, tuple(new_keys))
        # key "D" should not be attempted to be refreshed because it does not
        # have an origin.
        gpg_store.recv_keys.assert_has_calls(
            (mock.call(40*"A", keyserver="http://keyserver.dcc.sib.swiss:11371",
                       url_opener=urlopen),
             mock.call(40*"B", keyserver="keyserver2", url_opener=urlopen),
             mock.call(40*"C", keyserver="keyserver2", url_opener=urlopen)),
            any_order=True)
        # All keys must have been reloaded from the GPGstore.
        gpg_store.list_pub_keys.assert_called_once_with(
            keys=[40*c for c in ("A", "B", "C", "D")], sigs=...)

        # Check that when a keyserver is specified, all keys are attempted
        # to be refreshed.
        new_keys = crypt.refresh_keys(keys, gpg_store, sigs=...,
                                      keyserver_url=self.keyserver,
                                      url_opener=urlopen)
        # All keys must be attempted to be refreshed on the default keyserver.
        gpg_store.recv_keys.assert_has_calls(
            (mock.call(40*"A", keyserver=self.keyserver, url_opener=urlopen),
             mock.call(40*"B", keyserver=self.keyserver, url_opener=urlopen),
             mock.call(40*"C", keyserver=self.keyserver, url_opener=urlopen),
             mock.call(40*"D", keyserver=self.keyserver, url_opener=urlopen)),
            any_order=True)
        self.assertEqual(keys, tuple(new_keys))

        # Check that non-refreshed keys raise a warning.
        with self.assertWarns(UserWarning):
            crypt.refresh_keys(keys, gpg_store, sigs=...)

        # Check that duplicated keys are returned duplicated:
        keys_dups = (self.key1,) * 3
        gpg_store = new_gpg_store((self.key1,))
        new_keys = crypt.refresh_keys(keys_dups, gpg_store, sigs=...)
        self.assertEqual(keys_dups, tuple(new_keys))

        # Check that a missmatch between the number of keys in input and
        # the number of keys retrieved from the local keyring after the
        # refresh triggers an error.
        gpg_store = new_gpg_store(keys[1:])
        with self.assertRaises(RuntimeError):
            crypt.refresh_keys(keys, gpg_store, sigs=...)
        # Same as above, but this time the missmatch in only in one of the
        # fingerprints. The number of keys in input/output stays the same.
        gpg_store = new_gpg_store(
            (fake_key(fingerprint="0" + 39*"A"),) + keys[1:])
        with self.assertRaises(RuntimeError):
            crypt.refresh_keys(keys, gpg_store, sigs=...)

    def test_fingerprint2keyid(self):
        self.assertEqual(crypt.fingerprint2keyid(self.key1.fingerprint),
                         self.key1.key_id)
        with self.assertRaises(RuntimeError):
            crypt.fingerprint2keyid("AAA")


@contextmanager
def assert_conditional_raise(test: unittest.TestCase, error_type: Optional[Exception]):
    if error_type:
        with test.assertRaises(error_type):
            yield None
    else:
        yield None
