#!/usr/bin/env python3
"""Tests for ruinator.py"""

import os
import random
import re
import string
from subprocess import getstatusoutput

prg = './ruinator.py'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['', '-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert (rv > 0) if flag == '' else (rv == 0)
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def random_string():
    """generate a random filename"""

    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


# --------------------------------------------------
def test_bad_wordlist():
    """Test bad"""

    bad = random_string()
    rv, out = getstatusoutput(f'{prg} -w {bad} foo')
    assert rv != 0
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_pulp_fiction():
    """Test Pulp Fiction"""

    rv, out = getstatusoutput(f'{prg} "Pulp Fiction"')
    assert rv == 0
    assert out.rstrip() == '\n'.join(
        ['Pulp Fiction', 'Poulp Fiction', 'Pulp Friction', 'Pulpy Fiction'])
