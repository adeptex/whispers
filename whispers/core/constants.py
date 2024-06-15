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

REGEX_AST_FILE = compile(
    r"(py(thon)?|[jt]s|vue|java(script)?|kts?|scala|php|go(lang)?|c(pp|\+\+|s(harp)?|\#)?|lua|r[bs]?|clj|(g|prom)?ql|tf|proto|jsonnet|ocaml|hack|lisp|dart|julia|hcl|solidity|swift|(ap)?ex)[0-9]*$"
)
REGEX_AST_FILE_VERSION = compile(r"[0-9]*$")
MAP_AST_LANG = {
    "kts": "kotlin",
    "clj": "clojure",
    "cs": "csharp",
    "rb": "ruby",
    "rs": "rust",
}
