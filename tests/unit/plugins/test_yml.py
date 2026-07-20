import re
import time

import pytest

from whispers.plugins.yml import Yml

# Oracle: the original regex the linear scan replaces. Used only to assert
# behavioural equivalence on well-formed / edge inputs (never on the
# pathological inputs, where it is quadratic).
_REFERENCE = re.compile(r"[<{]%.*?%[}>]", flags=re.MULTILINE | re.DOTALL)


@pytest.mark.parametrize(
    "document",
    [
        "",
        "no markers here",
        "a {% if x %} b",
        "erb <%= foo %> bar",
        "{% a %}{% b %}{% c %}",
        "cross {%\nline %} end",
        "stray 50% off {% t %}",
        "dash {%- x -%} y",
        "percent inside {% a%b %} end",
        "<%c%d%> tail",
        "open only {% no close",
        "close only %} here",
        "mixed {% a %} and {{ b }}",
    ],
)
def test_strip_template_blocks_matches_reference(document):
    assert Yml._strip_template_blocks(document) == _REFERENCE.sub("", document)


@pytest.mark.parametrize(
    "document",
    [
        "{% x" * 200000,  # many unclosed {% ... quadratic for the old regex
        "{% a %}" * 200000,  # many balanced blocks
        "<% y" * 200000,  # many unclosed <%
    ],
)
def test_strip_template_blocks_is_linear(document):
    # The replaced regex was O(n^2) on these inputs and hung for a long time;
    # the linear scan must finish near-instantly.
    start = time.monotonic()
    Yml._strip_template_blocks(document)
    assert time.monotonic() - start < 5


def test_pairs_quotes_mustache_and_detects_secret(tmp_path):
    path = tmp_path / "custom.yml"
    path.write_text(
        "title: Site\n" "password: SuperSecret123456\n" "nav: {{ site.data.x }}\n" "block: {% if a %}yes{% endif %}\n"
    )
    values = [pair.value for pair in Yml().pairs(path)]
    assert "SuperSecret123456" in values


def test_pairs_does_not_hang_on_pathological_yaml(tmp_path):
    path = tmp_path / "patho.yml"
    path.write_text("a: " + "{{x" * 200000 + "\n")
    start = time.monotonic()
    list(Yml().pairs(path))
    assert time.monotonic() - start < 5
