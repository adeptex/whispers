from typing import Iterator

from whispers.core.utils import is_static
from whispers.models.pair import KeyValuePair


class Arn:
    def pairs(self, code: str) -> Iterator[KeyValuePair]:
        account = self.get_account_from_arn(code)
        if is_static("account", account):
            yield KeyValuePair("aws account", account, [code])

    def get_account_from_arn(code: str) -> str:
        if not code:
            return ""  # Empty

        if not code.startswith("arn:aws:"):
            return ""  # Not AWS ARN

        arn = code.split(":")

        if len(arn) < 5:
            return ""  # Missing AWS Account ID

        return arn[4]  # AWS Account ID
