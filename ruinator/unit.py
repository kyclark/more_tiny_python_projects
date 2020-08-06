import io
from ruinator import shorten, swap, read_file, ruin


# --------------------------------------------------
def test_shorten() -> None:
    """Test shorten"""

    assert shorten('abcd') == ['bcd', 'acd', 'abd', 'abc']


# --------------------------------------------------
def test_swap() -> None:
    """Test swap"""

    assert swap('Pulp Fiction'.split(), 'Friction', 1) == 'Pulp Friction'


# --------------------------------------------------
def test_read_file() -> None:
    """Test make_sig"""

    assert read_file(io.StringIO('start star')) == {
        'star': {'start'},
        'start': {'star'}
    }


# --------------------------------------------------
def test_ruin() -> None:
    """Test ruin"""

    pool = {'star': {'start'}, 'start': {'star'}}
    assert ruin('star', pool) == ['start']
    assert ruin('start', pool) == ['star']
