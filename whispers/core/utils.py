import re
import string
from base64 import b64decode
from pathlib import Path
from typing import List

from jellyfish import jaro_winkler_similarity
from luhn import verify as luhn_verify
from yaml import safe_load, safe_load_all

from whispers.core.log import global_exception_handler
from whispers.models.pair import KeyValuePair

DEFAULT_PATH = Path(__file__).parents[1]
DEFAULT_SEVERITY = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]

ESCAPED_CHARS = str.maketrans({"'": r"\'", '"': r"\""})

REGEX_URI = re.compile(r"[:\w\d]+://.+", flags=re.IGNORECASE)
REGEX_PATH = re.compile(r"^((([A-Z]|file|root):)?(\.+)?[/\\]+).*$", flags=re.IGNORECASE)
REGEX_IAC = re.compile(r"\![A-Za-z]+ .+", flags=re.IGNORECASE)
REGEX_PRIVKEY_FILE = re.compile(r"(rsa|dsa|ed25519|ecdsa|pem|crt|cer|ca-bundle|p7b|p7c|p7s|ppk|pkcs12|pfx|p12)")


def load_yaml_from_file(filepath: Path) -> dict:
    """Safe load yaml from given file path"""
    ret = safe_load(filepath.read_text())
    if not isinstance(ret, dict):
        return {}

    return ret


def truncate_all_space(value: str) -> str:
    """Replace multiple space characters by a single space character"""
    if not value:
        return ""

    return re.sub(r"\s+", " ", value)


def strip_string(value: str) -> str:
    """Strips leading and trailing quotes and spaces"""
    if not value:
        return ""

    return str(value).strip(" '\"\n\r\t")


def simple_string(value: str) -> str:
    """Returns a simplified value for loose comparison"""
    if not value:
        return ""

    value = strip_string(value)  # Remove quotes
    value = value.rstrip("\\")  # Remove trailing backslashes
    value = value.lower()  # Lowercase
    value = re.sub(r"[^a-z0-9]", "_", value.strip())  # Simplify

    return value


def similar_strings(a: str, b: str) -> float:
    """Returns similarity coefficient between two strings"""
    a = simple_string(a).replace("_", "")
    b = simple_string(b).replace("_", "")

    return jaro_winkler_similarity(a, b)


def is_ascii(data: str) -> bool:
    """Checks if given data is printable text"""
    if isinstance(data, bytes):
        try:
            data = data.decode("utf-8")
        except Exception:
            return False

    if not isinstance(data, (str, int)):
        return False

    for ch in str(data):
        if ch not in string.printable:
            return False

    return True


def is_base64(data: str) -> bool:
    """Checks if given data is base64-decodable to text"""
    if not isinstance(data, str):
        return False

    try:
        b64decode(data).decode("utf-8")
        return True

    except Exception:
        return False


def is_base64_bytes(data: str) -> bool:
    """Checks if given data is base64-decodable to bytes"""
    try:
        return b64decode(data) != b""

    except Exception:
        return False


def is_uri(data: str) -> bool:
    """Checks if given data resemples a URI"""
    if not is_ascii(data):
        return False

    if isinstance(data, int):
        return False

    if any(map(lambda ch: ch in data, string.whitespace)):
        return False

    if not REGEX_URI.match(data):
        return False

    return True


def is_path(data: str) -> bool:
    """Checks if given data resemples a system path"""
    if not is_ascii(data):
        return False

    if isinstance(data, int):
        return False

    if not REGEX_PATH.match(data):
        return False

    return True


def is_iac(data: str) -> bool:
    """Checks if given data resemples IaC function"""
    if not is_ascii(data):
        return False

    if isinstance(data, int):
        return False

    if not REGEX_IAC.match(data):
        return False

    return True


def is_luhn(data: str) -> bool:
    """Checks if given data resembles a credit card number"""
    if not is_ascii(data):
        return False

    if not str(data).isnumeric():
        return False

    return luhn_verify(str(data))


def is_similar(key: str, value: str, similarity: float) -> bool:
    """
    Checks similarity between key and value.
    Returns True if calculated similarity is greater than given similarity.
    """
    return similar_strings(key, value) >= similarity


def find_line_number(pair: KeyValuePair) -> int:
    """Finds line number using pair keypath and value"""
    if pair.line:
        return pair.line  # Already set

    valuepath = pair.value.split("\n")[0][:16]
    findpath = [*pair.keypath, valuepath]
    foundline = 0

    try:
        with Path(pair.file).open() as fh:
            for lineno, line in enumerate(fh, 1):
                founditems = 0

                for item in findpath:
                    if item not in line:
                        break

                    founditems += 1
                    foundline = lineno

                findpath = findpath[founditems:]

                if not findpath:
                    return foundline

    except Exception:  # pragma: no cover
        global_exception_handler(pair.file, "Failed parsing file")

    return 0


def default_rules() -> List[dict]:
    """Read and parse builtin rules"""
    rules = []
    files = DEFAULT_PATH.joinpath("rules").glob("*.yml")
    for file in files:
        list(map(rules.extend, safe_load_all(file.read_text())))

    return rules


def list_rule_prop(prop: str, rules: List[dict]) -> List[str]:
    """List rule property given a list of rules"""
    return sorted(set(map(lambda rule: rule[prop], rules)))
