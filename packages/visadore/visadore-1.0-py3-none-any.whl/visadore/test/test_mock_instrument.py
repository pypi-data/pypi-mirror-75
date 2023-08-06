from visadore import get
from pyvisa import ResourceManager
import os.path
import pytest
from hypothesis import given
from hypothesis.strategies import integers

YAML_FILENAME = "mock_instrument.yaml"
RESOURCES = ["ASRL1::INSTR", "ASRL2::INSTR"]
EXPECTED_FEATURES = []

yaml_dir = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(yaml_dir, YAML_FILENAME)
backend = "{}@sim".format(yaml_path)


@pytest.fixture(scope="session")
def get_instruments():
    rm = ResourceManager(backend)
    return [(resource_name, get(resource_name, rm)) for resource_name in RESOURCES]


def test_mock_unique_name(get_instruments):
    """Test that all of the instruments resources names are unique."""
    assert len(set([i.get_resource_name() for n, i in get_instruments])) == len(get_instruments)


@given(a=integers(min_value=0, max_value=100), b=integers(min_value=0, max_value=100))
def test_product_feature(a, b, get_instruments):
    """Test that the local product feature and the instrument product feature produce the same results."""
    name, instrument = get_instruments[0]
    assert instrument.local_product(a, b) == instrument.instr_product(a, b)
