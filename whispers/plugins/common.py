from itertools import chain
from typing import Iterator, Optional
from urllib.parse import parse_qsl, urlparse

from whispers.core.utils import is_static
from whispers.models.pair import KeyValuePair


class Common:
    """Checks text for common patterns, such as URI, AWS ARN, etc."""

    def pairs(self, value: str) -> Iterator[KeyValuePair]:
        if not value:
            return []  # Empty

        for word in value.split(" "):
            yield from self.parse_uri(word)
            yield from self.parse_arn(word)


    @staticmethod
    def parse_uri(text: str) -> Iterator[KeyValuePair]:
        """Check if text resembles a Uniform Resource Identifier (URI)"""
        if "://" not in text:
            return []  # Not URI

        uri = urlparse(text)

        yield KeyValuePair("URI", text, [text])

        if uri.password:
            yield KeyValuePair("uri_creds", f"{uri.username}:{uri.password}", [text])

        if uri.query:
            for key, value in parse_qsl(uri.query):
                yield KeyValuePair(key, value, [text])

    @staticmethod
    def parse_arn(text: str) -> Iterator[KeyValuePair]:
        """Check if text resembles an AWS ARN"""
        if not text.startswith("arn:aws:"):
            return []  # Not AWS ARN

        arn = text.split(":")

        if len(arn) < 5:
            return []  # Missing AWS Account ID

        account = arn[4]

        if is_static("account", account):
            yield KeyValuePair("aws_account", account, [text])

    @staticmethod
    def parse_pk(text: str) -> Iterator[KeyValuePair]:
        """Check if text resembles a Private Key (PK), only for plaintext files"""
        if not (text.startswith("-----") and text.endswith("-----")):
            return []

        if len(text) < 15:
            return []

        yield KeyValuePair("private_key", text)
