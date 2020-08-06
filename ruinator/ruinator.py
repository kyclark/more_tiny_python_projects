#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-02-17
Purpose: Ruin input text by adding/subtracting one letter
"""

import argparse
import re
from collections import defaultdict
from typing import NamedTuple, TextIO, Dict, Set, List


class Args(NamedTuple):
    text: str
    limit: int
    words_list: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Ruin input text by adding/subtracting one letter',
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
                        type=argparse.FileType('rt'),
                        default='/usr/share/dict/words')

    args = parser.parse_args()

    if args.limit < 0:
        parser.error(f'--limit "{args.limit}" must be > 0')

    return Args(args.text, args.limit, args.words)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    text = args.text.lower()

    if ruined := ruin(text, read_file(args.words_list)):
        print('\n'.join([text] + sorted(ruined)))
    else:
        print(f'Sorry, I could not find a way to ruin "{text}".')


# --------------------------------------------------
def ruin(text: str, pool: Dict[str, Set[str]]) -> List[str]:
    """Ruin it"""

    ruined = []

    for i, word in enumerate(text.lower().split()):
        if word in pool:
            for other in pool[word]:
                ruined.append(swap(text.split(), other, i))

    return ruined


# --------------------------------------------------
def read_file(fh: TextIO) -> Dict[str, Set[str]]:
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
                grouped[word].add(shorter)

    return grouped


# --------------------------------------------------
def swap(original: List[str], word: str, pos: int) -> str:
    """Swap out a word from the original"""

    original[pos] = word
    return ' '.join(original)


# --------------------------------------------------
def shorten(word: str) -> List[str]:
    """ Return shorter versions """

    shorter = []
    for i in range(len(word)):
        shorter.append(word[:i] + word[i + 1:])

    return shorter


# --------------------------------------------------
if __name__ == '__main__':
    main()
