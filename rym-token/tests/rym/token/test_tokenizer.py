#!/usr/bin/env python3
"""Test."""

import logging
from datetime import date, datetime, time, timedelta, timezone
from unittest import TestCase

import rym.token.tokenizer as MOD
from rym.token.structures import Token

LOGGER = logging.getLogger(__name__)


class ThisTestCase(TestCase):
    """Base test case for the module."""


class TestTokenize(ThisTestCase):
    """Test function."""

    maxDiff = None

    def test_words_and_punctuation_from_block_of_text(self) -> None:
        # NOTE: Intentionally did not used dedent.
        text = """
            Find all the words -- and punctuation. But we'll treat
            contractions as words: The meaning
            is lost if you split 'em up.
        """
        #   012345678901234567890123456789012345678901234567890123456789
        #   0         1         2         3         4         5
        expected = [
            Token(type="WORD", value="Find", line=1, column=12),
            Token(type="WORD", value="all", line=1, column=17),
            Token(type="WORD", value="the", line=1, column=21),
            Token(type="WORD", value="words", line=1, column=25),
            Token(type="PUNCTUATION", value="--", line=1, column=31),
            Token(type="WORD", value="and", line=1, column=34),
            Token(type="WORD", value="punctuation", line=1, column=38),
            Token(type="PUNCTUATION", value=".", line=1, column=49),
            Token(type="WORD", value="But", line=1, column=51),
            Token(type="WORD", value="we'll", line=1, column=55),
            Token(type="WORD", value="treat", line=1, column=61),
            Token(type="WORD", value="contractions", line=2, column=12),
            Token(type="WORD", value="as", line=2, column=25),
            Token(type="WORD", value="words", line=2, column=28),
            Token(type="PUNCTUATION", value=":", line=2, column=33),
            Token(type="WORD", value="The", line=2, column=35),
            Token(type="WORD", value="meaning", line=2, column=39),
            Token(type="WORD", value="is", line=3, column=12),
            Token(type="WORD", value="lost", line=3, column=15),
            Token(type="WORD", value="if", line=3, column=20),
            Token(type="WORD", value="you", line=3, column=23),
            Token(type="WORD", value="split", line=3, column=27),
            Token(type="PUNCTUATION", value="'", line=3, column=33),
            Token(type="WORD", value="em", line=3, column=34),
            Token(type="WORD", value="up", line=3, column=37),
            Token(type="PUNCTUATION", value=".", line=3, column=39),
        ]
        result = MOD.tokenize(text)
        found = list(result)
        self.assertEqual(expected, found)

    def test_matches_quotation(self) -> None:
        # NOTE: Intentionally did not used dedent.
        #   0         1         2         3         4         5
        #   012345678901234567890123456789012345678901234567890123456789
        text = """
            "Well", he said, "I hadn't really thought about it".
        """
        expected = [
            Token(type="QUOTE", value='"Well"', line=1, column=12),
            Token(type="PUNCTUATION", value=",", line=1, column=18),
            Token(type="WORD", value="he", line=1, column=20),
            Token(type="WORD", value="said", line=1, column=23),
            Token(type="PUNCTUATION", value=",", line=1, column=27),
            Token(
                type="QUOTE",
                value='"I hadn\'t really thought about it"',
                line=1,
                column=29,
            ),
            Token(type="PUNCTUATION", value=".", line=1, column=63),
        ]
        result = MOD.tokenize(text)
        found = list(result)
        self.assertEqual(expected, found)

    def test_matches_numbers(self) -> None:
        #   0         1         2         3         4         5         6
        #   0123456789012345678901234567890123456789012345678901234567890123456789
        text = """
            Some numbers are floating point, such as 2_000.0, 3.14, and 1e-3,
            and others that are integers, such as -4, 1, 42, and 1,005.
        """
        spec = [MOD.integer(), MOD.number()]
        buf = 12
        expected = [
            Token(type="NUMBER", value=2000.0, line=1, column=41 + buf),
            Token(type="NUMBER", value=3.14, line=1, column=50 + buf),
            Token(type="NUMBER", value=0.001, line=1, column=60 + buf),
            Token(type="INTEGER", value=-4, line=2, column=38 + buf),
            Token(type="INTEGER", value=1, line=2, column=42 + buf),
            Token(type="INTEGER", value=42, line=2, column=45 + buf),
            Token(type="INTEGER", value=1005, line=2, column=53 + buf),
        ]
        result = MOD.tokenize(text, spec)
        found = list(result)
        self.assertEqual(expected, found)

    def test_matches_dates(self) -> None:
        # NOTE: Test all dates together to ensure each can be detected.
        #   0         1         2         3         4         5         6
        #   0123456789012345678901234567890123456789012345678901234567890123456789
        text = """
            Dates are often expressed as timestamps: 2008-07-25T02:45:00.000000-05:00
            But there are quite a few variations:
                2008-07-25T02:45:00.000000-05:00
                2008-07-25T02:45:00.000
                2008-07-25 02:45
                2008-07-25T02:45:00.000000Z
            But you can also only specify the date: 1985-10-26, 1955.11.05, 2015/10/21
            Or just the time: 21:00 in 24-hour or 9:00 PM in 12-hour formats.
            Time can also include a timezone: 04:20Z, 16:20-06:00
        """
        spec = [MOD.timestamp(), MOD.date(), MOD.time()]  # ORDER MATTERS!
        buf = 12
        arg = (2008, 7, 25, 2, 45)
        expected = [
            Token(
                type="TIMESTAMP",
                value=datetime(*arg, tzinfo=timezone(timedelta(hours=-5))),
                line=1,
                column=41 + buf,
            ),
            Token(
                type="TIMESTAMP",
                value=datetime(*arg, tzinfo=timezone(timedelta(hours=-5))),
                line=3,
                column=4 + buf,
            ),
            Token(type="TIMESTAMP", value=datetime(*arg), line=4, column=4 + buf),
            Token(type="TIMESTAMP", value=datetime(*arg), line=5, column=4 + buf),
            Token(
                type="TIMESTAMP",
                value=datetime(*arg, tzinfo=timezone.utc),
                line=6,
                column=4 + buf,
            ),
            Token(type="DATE", value=date(1985, 10, 26), line=7, column=40 + buf),
            Token(type="DATE", value=date(1955, 11, 5), line=7, column=52 + buf),
            Token(type="DATE", value=date(2015, 10, 21), line=7, column=64 + buf),
            Token(type="TIME", value=time(21, 0, 0), line=8, column=18 + buf),
            Token(type="TIME", value=time(21, 0, 0), line=8, column=38 + buf),
            Token(
                type="TIME",
                value=time(4, 20, 0, tzinfo=timezone.utc),
                line=9,
                column=34 + buf,
            ),
            Token(
                type="TIME",
                value=time(16, 20, 0, tzinfo=timezone(timedelta(hours=-6))),
                line=9,
                column=42 + buf,
            ),
        ]
        result = MOD.tokenize(text, spec)
        found = list(result)
        self.assertEqual(expected, found)


# __END__
