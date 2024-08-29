import pytest
from unittest.mock import Mock
from ch9329.config import *


def test_set_device_descriptors_raises_for_too_long_descriptor():
    with pytest.raises(ValueError):
        ser = Mock()
        set_device_descriptors(
            ser, USBStringDescriptor.MANUFACTURER, "long" * 50
        )
