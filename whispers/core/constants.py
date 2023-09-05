import re
from pathlib import Path

DEFAULT_PATH = Path(__file__).parents[1]

DEFAULT_SEVERITY = ["Critical", "High", "Medium", "Low", "Info"]

ESCAPED_CHARS = str.maketrans({"'": r"\'", '"': r"\""})

REGEX_URI = re.compile(r"[:\w\d]+://.+", flags=re.IGNORECASE)
REGEX_PATH = re.compile(r"^((([A-Z]|file|root):)?(\.+)?[/\\]+).*$", flags=re.IGNORECASE)
REGEX_IAC = re.compile(r"\![A-Za-z]+ .+", flags=re.IGNORECASE)
REGEX_PRIVKEY_FILE = re.compile(r"(rsa|dsa|ed25519|ecdsa|pem|crt|cer|ca-bundle|p7b|p7c|p7s|ppk|pkcs12|pfx|p12)")
REGEX_ENVVAR = re.compile(r"^\$\$?\{?[A-Z0-9_]+\}?$")
