"""How a quote is matched against a clause. Shared by validation and the site highlighter.

A quote matches if, after collapsing runs of whitespace (line breaks in the clause text are
layout), it is an exact substring of the clause. A model may shorten a long quote with "..."
or "…": then every fragment must appear, verbatim and in order, and be at least 3 words long.
Nothing else is forgiven: a changed word, letter case, or punctuation mark does not match.
"""
import re

ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*")


def ws(s):
    return re.sub(r"\s+", " ", s).strip()


def spans(quote, text):
    """[(start, end)] in ws(text) for each fragment of the quote, or None if it doesn't match."""
    t = ws(text)
    frags = [ws(f) for f in ELLIPSIS.split(quote) if f.strip()]
    if not frags or (len(frags) > 1 and any(len(f.split()) < 3 for f in frags)):
        return None
    out, pos = [], 0
    for f in frags:
        i = t.find(f, pos)
        if i < 0:
            return None
        out.append((i, i + len(f)))
        pos = i + len(f)
    return out


def matches(quote, text):
    return spans(quote, text) is not None
