from pathlib import Path
from re import IGNORECASE, compile

DEFAULT_PATH = Path(__file__).parents[1]

DEFAULT_SEVERITY = ["Critical", "High", "Medium", "Low", "Info"]

ESCAPED_CHARS = str.maketrans({"'": r"\'", '"': r"\""})

REGEX_URI = compile(r"[:\w\d]+://.+", flags=IGNORECASE)
REGEX_PATH = compile(r"^((([A-Z]|file|root):)?(\.+)?[/\\]+).*$", flags=IGNORECASE)
REGEX_IAC = compile(r"\![A-Za-z]+ .+", flags=IGNORECASE)
REGEX_PRIVKEY_FILE = compile(r"(rsa|dsa|ed25519|ecdsa|pem|crt|cer|ca-bundle|p7b|p7c|p7s|ppk|pkcs12|pfx|p12)")
REGEX_ENVVAR = compile(r"^\$\$?\{?[A-Z0-9_]+\}?$")
REGEX_SEMVER = compile(r"^[\^~\-=vV<>]{0,3}([0-9]+\.){1,2}[0-9]+(\-.*)?$")
