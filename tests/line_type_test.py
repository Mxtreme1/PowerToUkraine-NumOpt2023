from src.line_type import LineType

import pytest


def test_line_type_sanity():
    type_a = LineType("CoolType", None)

    assert type_a.name == "CoolType"
    assert type_a.rating is None


def test_stupid_type_name():
    with pytest.raises(AssertionError):
        LineType("Stupid Type", None)


def test_change_name():
    type_a = LineType("CoolType", None)

    assert type_a.name == "CoolType"
    assert type_a.rating is None

    type_a.id = 100

    type_a.name = "OtherCoolType"

    assert type_a.name == "OtherCoolType"
    assert type_a.rating is None


def test_change_rating_to_none():
    type_a = LineType("CoolType", None)

    assert type_a.name == "CoolType"
    assert type_a.rating is None

    type_a.rating = None

    assert type_a.name == "CoolType"
    assert type_a.rating is None
