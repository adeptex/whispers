from itertools import chain
from typing import Iterator, List
from urllib.parse import parse_qsl, urlparse

from whispers.models.pair import KeyValuePair


class Common:
    """Checks text for common patterns, such as URI, AWS ARN, etc."""

    def __init__(self, keypath: List = [], line: int = 0) -> None:
        self.keypath = keypath
        self.line = line

    def pairs(self, value: str) -> Iterator[KeyValuePair]:
        """Check for common patterns in text"""
        if not value:
            return []  # Empty

        if not isinstance(value, str):
            return []  # Not a string

        words = value.split(" ")
        uris = map(self.parse_uri, words)
        arns = map(self.parse_arn, words)
        parsed = chain.from_iterable([*uris, *arns])
        yield from parsed

    def parse_uri(self, text: str) -> Iterator[KeyValuePair]:
        """Check if text resembles a Uniform Resource Identifier (URI)"""
        if "://" not in text:
            return []  # Not URI

        uri = urlparse(text)

        if uri.password:
            yield KeyValuePair("uri_creds", f"{uri.username}:{uri.password}", [*self.keypath, text])

        if uri.query:
            for key, value in parse_qsl(uri.query):
                yield KeyValuePair(key, value, [*self.keypath, text], line=self.line)

    def parse_arn(self, text: str) -> Iterator[KeyValuePair]:
        """Check if text resembles an AWS ARN"""
        if not text.startswith("arn:aws:"):
            return []  # Not AWS ARN

        arn = text.split(":")

        if len(arn) < 5 or not arn[4]:
            return []  # Missing AWS Account ID

        account = str(arn[4])

        yield KeyValuePair("aws_account", account, [*self.keypath, text], line=self.line)
