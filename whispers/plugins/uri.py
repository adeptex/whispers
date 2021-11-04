from typing import Iterator
from urllib.parse import parse_qsl, urlparse

from whispers.models.pair import KeyValuePair


class Uri:
    def pairs(self, code: str) -> Iterator[KeyValuePair]:
        uri = urlparse(code)
        if uri.password:
            yield KeyValuePair("uri creds", f"{uri.username}:{uri.password}", [code])

        if uri.query:
            for key, value in parse_qsl(uri.query):
                yield KeyValuePair(key, value, [code])
