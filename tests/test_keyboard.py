import pytest
from unittest.mock import Mock
from ch9329.keyboard import *


def test_trigger_keys_raises_for_too_many_keys():
    with pytest.raises(TooManyKeysError):
        ser = Mock()
        trigger_keys(ser, ["a", "b", "c", "d", "e", "f", "g"])
