from hypothesis import given
from hypothesis.strategies import text, characters
from visadore.identity import Identity
from visadore.identity import _identity_parser
import pytest


KNOWN_IDNs = [
    (
        "TEKTRONIX,TBS1102C,Q000008,CF:91.1CT FV:v1.28.280; FPGA:v20.71; \n",
        Identity(
            "TEKTRONIX",
            "TBS1102C",
            "Q000008",
            "CF:91.1CT FV:v1.28.280; FPGA:v20.71;",
        ),
    ),
    (
        "TEKTRONIX,MSO68B,PQ200008,CF:91.1CT FV:1.27.25.98\n",
        Identity(
            "TEKTRONIX",
            "MSO68B",
            "PQ200008",
            "CF:91.1CT FV:1.27.25.98",
        ),
    ),
]


def make_identity_string(company, model, serial, config):
    return ",".join([company, model, serial, config])


@given(
    text(alphabet=characters(blacklist_categories=["Cs"], blacklist_characters=[","])),
    text(alphabet=characters(blacklist_categories=["Cs"], blacklist_characters=[","])),
    text(alphabet=characters(blacklist_categories=["Cs"], blacklist_characters=[","])),
    text(alphabet=characters(blacklist_categories=["Cs"], blacklist_characters=[","])),
)
def test_identity_parser(company, model, serial, config):
    identity_nt = Identity(company, model, serial, config)
    identity_str = make_identity_string(company, model, serial, config)
    assert _identity_parser(identity_str) == identity_nt


@pytest.mark.parametrize("idn_string, expected", KNOWN_IDNs)
def test_known_idn_queries(idn_string, expected):
    test_string = idn_string.strip()
    assert _identity_parser(test_string) == expected
