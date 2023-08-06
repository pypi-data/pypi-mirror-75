from dataclasses import dataclass, field, fields, asdict as dataclass_asdict
from datetime import datetime
import re
from typing import List, Callable
from functools import wraps, lru_cache

from .lib.deserialize import deserialize
from .dpkg import METADATA_FILE


def new_str_type(converter: Callable) -> Callable:
    """Turns a function into a parametrizable str subtype (cached)"""
    @wraps(converter)
    @lru_cache(maxsize=None)
    def t(*args, **kwargs):
        c = converter(*args, **kwargs)

        G = type(converter.__name__, (str,), {
            "__new__": lambda _cls, arg: str(c(arg))})
        return G
    return t


@new_str_type
def HexStr(min_bits: int, max_bits: int = None):
    regex = r"[0-9A-Fa-f]{" + str(min_bits // 4)
    if max_bits is not None:
        regex += r"," + str(max_bits // 4)
    regex += r"}"

    def new(s):
        if not re.fullmatch(regex, s):
            rng = str(min_bits)
            if max_bits:
                rng += f"-{max_bits}"
            raise ValueError(f"Invalid hex string (length: {rng}): {s}")
        return s
    return new


@new_str_type
def AlnumStr(min_length: int,
             max_length: int,
             allow_dots: bool = False) -> Callable:
    """Generate a 'type definition' function that will check that a string is
    composed only of alphanumeric characters, dashes and underscores, and has
    a length between min_length and max_length.

    :param min_length: minimum length of string type.
    :param max_length: maximum length of string type.
    :param allow_dots: if True, dots are also allowed in the string type.
    :return: 'type definition' function.
    :raises ValueError:
    """
    regexp = r"[0-9A-Za-z" + (r"." if allow_dots else r"") + r"_-]{" + \
             str(min_length) + r"," + str(max_length) + r"}"

    def _alnum_str(string_to_check):
        if not re.fullmatch(regexp, string_to_check):
            raise ValueError(
                f"Invalid alphanumeric string: '{string_to_check}'. "
                f"This string can only contain alphanumeric characters, "
                f"{'dots, ' if allow_dots else ''}dashes and underscores. "
                f"It must have a length between {min_length} and "
                f"{max_length} characters."
            )
        return string_to_check
    return _alnum_str


ProjectIdStr = AlnumStr(3, 32, False)

DATE_FMT = "%Y-%m-%dT%H:%M:%S%z"


@dataclass(frozen=True)
class MetaData:
    projectID: ProjectIdStr
    sender: HexStr(128, 1024)
    recipients: List[HexStr(128, 1024)]
    checksum: HexStr(256)
    timestamp: datetime = field(
        metadata={
            "deserialize": lambda s: datetime.strptime(s, DATE_FMT),
            "serialize": lambda d: datetime.strftime(d, DATE_FMT)},
        default_factory=lambda: datetime.now().astimezone())
    version: str = "0.6"
    checksum_algorithm: str = "SHA256"
    compression_algorithm: str = "gzip"

    @classmethod
    def from_dict(cls, d: dict):
        # Downward compatibility to version 0.5:
        recipient = d.pop("recipient", None)
        if recipient:
            d["recipients"] = recipient
        sha256sum = d.pop("sha256sum", None)
        if sha256sum:
            d["checksum"] = sha256sum
            d["checksum_algorithm"] = "SHA256"

        try:
            return deserialize(cls)(d)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid {METADATA_FILE}: {e}")

    @classmethod
    def asdict(cls, m):
        d = dataclass_asdict(m)
        for f in fields(cls):
            ser = f.metadata.get("serialize")
            if ser is not None:
                d[f.name] = ser(d[f.name])
        return d
