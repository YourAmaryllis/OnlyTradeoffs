"""Turn an archived official source into a measure file (the clauses the models read).

Sources are saved unchanged in elections/<id>/sources/ and fingerprinted. This
script reads them, never edits them, and writes:

  measures/<measure_id>.json      {"measure_id", "clauses": [{"id", "text"}], "current_law", "source"}
  sources/<name>.import-log.txt   every change made to the source's text, so anyone can check it

Supported sources:
  --pdf   a filed initiative (Attorney General PDF). These are scans. By default (--ocr vote) the
          text is read three ways (Tesseract, RapidOCR, the PDF's own OCR layer) and voted word by
          word by tools/ocr_vote.py; the raw readings are kept in sources/ocr/. Then only mechanical
          fixes are applied, and each is logged:
            - page furniture removed: page footers ("Page 3 of 8"), running titles, the
              cover letter before --start
            - lines joined into paragraphs; a line ending in "-" is joined without a space
              (the hyphen is kept)
            - "( c)" -> "(c)": a space read inside a subdivision letter
            - "(0)" -> "(o)": subdivisions are never numbered zero
            - "ofall" -> "of all": "of" read as joined to the next word, only when the
              joined form is not itself an English word (checked against /usr/share/dict/words)
            - a subdivision label misread as "(1)", "(I)", "(0)" or "G)" is corrected only when the
              measure's own lettering leaves exactly that letter missing ("(k) (1) (m)" -> "(l)")
          Any other OCR error is left as read; the page links the scan for comparison.
  --html  a legislative measure page from leginfo.legislature.ca.gov (bill text only;
          the Legislative Counsel's Digest is a summary and is dropped)

Clauses follow the measure's own numbering: top-level sections (Sec. 1, Sec. 2, ...),
and inside them the sections of any code or constitutional article being added.

Usage:
  python3 tools/import_measure.py --pdf <file> --start "<first line of the law>" --prefix "Prop 40" \
      --measure-id CA-2026-P40 --out elections/ca-2026-11/measures/CA-2026-P40.json --url <official url>
  python3 tools/import_measure.py --html <file> --prefix "Prop 43" ... (same)
"""
import argparse
import hashlib
import html as htmllib
import json
import re
from datetime import date
from pathlib import Path

import sys

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
WORDS = set(w.strip().lower() for w in open("/usr/share/dict/words")) if Path("/usr/share/dict/words").exists() else set()

TOP = re.compile(r"^(?:Sec\.|Section|SECTION) (\d+)\.(?=\s|$)")
SUB = re.compile(r"^(?:SECTION|SEC\.|Sec\.) (\d+(?:\.\d+)?)\.(?=\s|$)")
CODE = re.compile(r"^(\d{4,6}(?:\.\d+)?)\.(?=\s|$)")
FOOTER = re.compile(r"^(Page ?\d+ ?of ?\d+|.*\bPage ?\d+ ?of ?\d+|Initiative \d\d-\d{4}.*)$")


class Log:
    def __init__(self):
        self.lines = []

    def add(self, rule, before, after=""):
        self.lines.append(f"{rule}: {before!r}" + (f" -> {after!r}" if after else ""))


def pdf_lines(path, log):
    lines = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            for l in (page.extract_text() or "").splitlines():
                l = l.strip()
                if not l:
                    continue
                if FOOTER.match(l):
                    log.add(f"p{i} furniture removed", l)
                    continue
                lines.append(l)
    return lines


def ocr_fixes(text, log):
    def subdiv(m):
        log.add("subdivision spacing", m.group(0), f"({m.group(1)})")
        return f"({m.group(1)})"
    text = re.sub(r"\( ?([a-z0-9]{1,4}) ?\)", lambda m: subdiv(m) if " " in m.group(0) else m.group(0), text)

    def zero(m):   # subdivisions are never numbered zero: "(0)" is the letter o
        log.add("'(0)' is the letter o", m.group(0), "(o)")
        return "(o)"
    text = re.sub(r"\(0\)", zero, text)

    def of_join(m):
        w = m.group(0)
        if w.lower() in WORDS or not WORDS:
            return w
        log.add("'of' split", w, f"of {w[2:]}")
        return f"of {w[2:]}"
    text = re.sub(r"\bof[a-z]{2,}\b", of_join, text)

    def of_cap(m):
        log.add("'of' split", m.group(0), f"of {m.group(1)}")
        return f"of {m.group(1)}"
    text = re.sub(r"\bof([A-Z][a-z]+)", of_cap, text)
    if "\u00ad" in text:
        log.add("soft hyphen removed", text[max(0, text.index("\u00ad") - 20):text.index("\u00ad") + 10])
        text = text.replace("\u00ad", "-")
    return text


AMBIG = {"(1)": "l", "(I)": "l", "(l)": "l", "(0)": "o", "(o)": "o", "G)": "j", "(!)": "l", "(|)": "l"}


def repair_labels(paras, log):
    """Fix OCR confusions in subdivision labels using the measure's own lettering.
    A paragraph starting with "(1)", "(I)", "(0)" or "G)" is read as the letter that the sequence
    needs, only when the previous letter label and the next one leave exactly that letter missing
    (e.g. "(k) ... (1) ... (m)" -> "(l)"). Anything else is left alone."""
    lab = re.compile(r"^(\([a-z0-9!|I]{1,2}\)|G\))\s")
    letters = [(i, m.group(1)) for i, p in enumerate(paras) if (m := lab.match(p))]

    def letter(tok):
        m = re.fullmatch(r"\(([a-z])\)", tok)
        return m.group(1) if m else None
    for n, (i, tok) in enumerate(letters):
        if tok not in AMBIG or letter(tok) == AMBIG[tok] and tok == f"({AMBIG[tok]})":
            continue
        want = AMBIG[tok]
        prev = next((letter(t) for _, t in reversed(letters[:n]) if letter(t) and letter(t) not in "il"), None)
        nxt = next((letter(t) for _, t in letters[n + 1:] if letter(t) and letter(t) not in "il"), None)
        prev = prev or (letters[n - 1][1][1] if n and letter(letters[n - 1][1]) else None)
        if prev and nxt and ord(prev) + 1 == ord(want) and ord(nxt) - 1 == ord(want):
            fixed = f"({want})"
            if tok != fixed:
                paras[i] = fixed + paras[i][len(tok):]
                log.add("subdivision label from sequence", f"{tok} between ({prev}) and ({nxt})", fixed)
    return paras


def join(lines):
    """Lines -> paragraphs. A new paragraph starts at a heading or a subdivision marker."""
    starts = re.compile(r"^(\([a-zA-Z0-9]{1,4}\)\s|ARTICLE |Article [IVXL]+$|Art\. \d|PART |CHAPTER |Sec\.|SEC\.|SECTION|Section \d+\.|\d{4,6}(\.\d+)?\.(\s|$))")
    paras = []
    for l in lines:
        # A line can begin with a section number that is really the end of a cross-reference
        # ("... residency is determined under Sections" / "50308. ..."): only treat it as a
        # heading unless the previous paragraph ends mid-reference.
        if paras and CODE.match(l) and re.search(r"\b(Sections?|and|or|of|to|under|in|by|through)$", paras[-1]):
            paras[-1] += " " + l
            continue
        if not paras or starts.match(l):
            paras.append(l)
        elif paras[-1].endswith("-"):
            paras[-1] += l
        else:
            paras[-1] += " " + l
    return paras


def segment(paras, prefix):
    """Paragraphs -> clauses, by the measure's own numbering. Numbers must run in order,
    which keeps a cross-reference that happens to start a line from opening a clause."""
    clauses, top, sub, code = [], 0, None, 0
    cur = None

    def open_clause(cid, p):
        nonlocal cur
        cur = {"id": cid, "text": p}
        clauses.append(cur)

    for p in paras:
        m = TOP.match(p)
        if m and int(m.group(1)) == top + 1:
            top, sub, code = int(m.group(1)), None, 0
            open_clause(f"{prefix} Sec. {top}", p)
            continue
        m = SUB.match(p)
        if m and cur and (sub is None or float(m.group(1)) > float(sub)):
            sub = m.group(1)
            open_clause(f"{prefix} Sec. {top} §{sub}" if top else f"{prefix} §{sub}", p)
            continue
        m = CODE.match(p)
        if m and top and code < float(m.group(1)) <= (code + 5 if code else 1e9):
            code = float(m.group(1))
            open_clause(f"{prefix} Sec. {top} §{m.group(1)}", p)
            continue
        if cur is None:
            open_clause(f"{prefix} Preamble", p)
        else:
            cur["text"] += "\n" + p
    # A top-level section that only says where new text goes ("Sec. 6. Part 27 is added to
    # Division 2 ..., to read:") isn't a rule by itself: it heads the next clause.
    merged = []
    for c in clauses:
        if merged and re.search(r"to read:", merged[-1]["text"]) and len(merged[-1]["text"].split()) < 80 \
                and c["id"].startswith(merged[-1]["id"] + " §"):
            head = merged.pop()
            c = {"id": c["id"], "text": head["text"] + "\n" + c["text"]}
        merged.append(c)
    return merged


def split_subdivisions(clauses):
    """Split each clause at its top-level subdivisions (a), (b), ... (for short measures
    that are one section long, so each rule gets its own clause ID)."""
    out = []
    for c in clauses:
        parts = re.split(r"\n(?=\([a-z]\) )", c["text"])
        if len(parts) == 1:
            out.append(c)
            continue
        head, rest = (parts[0], parts[1:]) if not re.match(r"\([a-z]\) ", parts[0]) else (None, parts)
        if head and not re.fullmatch(r"(SEC\.|Sec\.|SECTION) [\d.]+\.", head.strip()):  # a bare heading isn't a clause
            out.append({"id": c["id"], "text": head})
        for part in rest:
            out.append({"id": f"{c['id']}{part[:3]}", "text": part})
    return out


def from_pdf(path, start, log, ocr="layer"):
    if ocr == "vote":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from ocr_vote import vote
        lines = []
        for page, plines, decisions in vote(path, Path(path).parent / "ocr"):
            for kind, before, after in decisions:
                log.add(f"p{page} OCR {kind}", before, after)
            for l in plines:
                l = l.strip()
                if not l:
                    continue
                if FOOTER.match(l) or re.search(r"Page ?[\dIl|]+ ?of ?\d+", l):
                    log.add(f"p{page} furniture removed", l)
                    continue
                lines.append(l)
    else:
        lines = pdf_lines(path, log)
    i = next(i for i, l in enumerate(lines) if l.startswith(start))
    log.add("cover letter and filing pages removed", f"{i} lines before {start!r}")
    lines = lines[i:]
    # trailing pages with no text (signature scans) give OCR noise: stop at the last line ending a sentence
    while lines and not re.search(r"[.:;)]$", lines[-1]):
        log.add("trailing OCR noise removed", lines.pop())
    return repair_labels(join([ocr_fixes(l, log) for l in lines]), log)


def from_html(path, log):
    raw = Path(path).read_text()
    # The bill text is the <span class="Resolution"> (or "Bill") block after the hidden "Bill Text" heading;
    # everything before it is the Legislative Counsel's Digest (a summary) and page navigation.
    i = raw.index("<h2>Bill Text</h2>")
    body = raw[i + len("<h2>Bill Text</h2>"):]
    body = body[:body.index('<div id="footer"')] if '<div id="footer"' in body else body
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r"<(br|/p|div|/div|/h\d|/li)[^>]*>", "\n", body)
    text = htmllib.unescape(re.sub(r"<[^>]+>", "", body))
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.splitlines()]
    lines = [l for l in lines if l]
    log.add("kept bill text only", "Legislative Counsel's Digest and page navigation dropped")
    return join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pdf")
    g.add_argument("--html")
    ap.add_argument("--start", help="first line of the law (pdf); everything before it is the cover letter")
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--measure-id", required=True)
    ap.add_argument("--url", required=True, help="official URL the source was fetched from")
    ap.add_argument("--fetched", default=str(date.today()))
    ap.add_argument("--current-law", default=None)
    ap.add_argument("--ocr", choices=["layer", "vote"], default="vote",
                    help="pdf text: the PDF's own text layer, or a 3-way vote (Tesseract, RapidOCR, layer)")
    ap.add_argument("--split-subdivisions", action="store_true", help="one clause per (a), (b), ... subdivision")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    src = Path(a.pdf or a.html).resolve()
    log = Log()
    paras = from_pdf(src, a.start, log, a.ocr) if a.pdf else from_html(src, log)
    clauses = segment(paras, a.prefix)
    if a.split_subdivisions:
        clauses = split_subdivisions(clauses)
    measure = {
        "measure_id": a.measure_id,
        "clauses": clauses,
        "current_law": a.current_law,
        "source": {"url": a.url, "archived": str(src.relative_to(ROOT)) if src.resolve().is_relative_to(ROOT) else str(src),
                   "sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "fetched_at": a.fetched,
                   "import_log": str(src.with_suffix(".import-log.txt").name)},
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(measure, indent=2, ensure_ascii=False) + "\n")
    src.with_suffix(".import-log.txt").write_text(
        f"Import log for {src.name} (sha256 {measure['source']['sha256']})\n"
        f"Source: {a.url}\nTool: tools/import_measure.py\n\n" + "\n".join(log.lines) + "\n")
    words = sum(len(c["text"].split()) for c in clauses)
    print(f"{a.measure_id}: {len(clauses)} clauses, {words} words, {len(log.lines)} logged changes → {a.out}")
