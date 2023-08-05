from typing import Tuple

import pytest

from coiled.utils import parse_identifier, ParseIdentifierError


@pytest.mark.parametrize(
    "identifier,expected",
    [
        ("coiled/xgboost", ("coiled", "xgboost")),
        ("xgboost", (None, "xgboost")),
        ("coiled/xgboost-py37", ("coiled", "xgboost-py37")),
        ("xgboost_py38", (None, "xgboost_py38")),
    ],
)
def test_parse_good_names(identifier, expected: Tuple[str, str]):
    account, name = parse_identifier(identifier, "name_that_would_be_printed_in_error")
    assert (account, name) == expected


@pytest.mark.parametrize(
    "identifier",
    ["coiled/dan/xgboost", "coiled/dan?xgboost", "dan\\xgboost", "jimmy/xgbóst", "",],
)
def test_parse_bad_names(identifier):
    with pytest.raises(ParseIdentifierError) as e:
        parse_identifier(identifier, "software_environment")
    assert "software_environment" in e.value.args[0]
