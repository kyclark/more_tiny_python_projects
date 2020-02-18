#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-02-17
Purpose: Ruin a phrase by adding one letter
"""

import argparse
import io
import os
import re
import sys
from collections import Counter, defaultdict


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Ruin a phrase by adding one letter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text', metavar='str', help='Input text')

    parser.add_argument('-l',
                        '--limit',
                        help='Limit output',
                        metavar='int',
                        type=int,
                        default=10)

    parser.add_argument('-w',
                        '--words',
                        help='Words file',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        default='/usr/share/dict/words')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    text = args.text
    pool = read_file(args.words)
    ruined = []

    for i, word in enumerate(text.lower().split()):
        if word in pool:
            for other in pool[word]:
                ruined.append(swap(text, other.title(), i))

    if ruined:
        print('\n'.join([text] + sorted(ruined)))
    else:
        print(f'Could not find a way to ruin "{text}". Sorry')


# --------------------------------------------------
def read_file(fh):
    """Read file into unique set of words"""

    words = set()

    for line in map(str.lower, fh):
        for word in map(lambda w: re.sub('[^a-z]', '', w), line.split()):
            words.add(word)

    grouped = defaultdict(set)
    for word in words:
        for shorter in shorten(word):
            if shorter in words:
                grouped[shorter].add(word)

    return grouped


# --------------------------------------------------
def swap(original, word, pos):
    """Swap out a word from the original"""

    original = original.split()
    original[pos] = word
    return ' '.join(original)


# --------------------------------------------------
def shorten(word):
    """ Return shorter versions """

    shorter = []
    for i in range(len(word)):
        shorter.append(word[:i] + word[i + 1:])

    return shorter


# --------------------------------------------------
def test_shorten():
    """Test shorten"""

    assert shorten('abcd') == ['bcd', 'acd', 'abd', 'abc']


# --------------------------------------------------
def test_swap():
    """Test swap"""

    assert swap('Pulp Fiction', 'Friction', 1) == 'Pulp Friction'


# --------------------------------------------------
def test_read_file():
    """Test make_sig"""

    assert read_file(io.StringIO('start star')) == {'star': {'start'}}


# --------------------------------------------------
if __name__ == '__main__':
    main()
