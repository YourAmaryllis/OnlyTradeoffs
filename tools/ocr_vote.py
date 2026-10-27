"""Read a scanned filing three independent ways and keep, word by word, what two of them agree on.

Readers:
  T  Tesseract 5 (github.com/tesseract-ocr/tesseract), page images at 300 dpi, --psm 4
  R  RapidOCR (PaddleOCR detection + recognition models, run with ONNX)
  L  the text layer already inside the PDF (the filer's or scanner's own OCR)

T is the backbone (it keeps line breaks and typographic quotes and dashes). For every stretch
where T disagrees with R or L:
  - if T agrees with either one, T stands
  - else if R and L agree, theirs replaces T's
  - else (all three differ) the reading closest to the other two wins if it clearly does
    (e.g. T "3™", R "3rd", L "3rc1" -> "3rd"); otherwise T stands. Logged as unresolved.
Agreement ignores differences that aren't the words themselves: curly vs straight quotes,
the various dashes, and spaces inside a word ("ofthe" = "of the").

Every page's raw readings are saved under <out_dir>/<pdf stem>/, and every replacement and
unresolved stretch is returned for the import log, so anyone can check a decision against the scan.

Usage (normally called by import_measure.py --ocr vote):
  python3 tools/ocr_vote.py <pdf> <out_dir>
"""
import difflib
import re
import subprocess
import sys
from pathlib import Path

import pdfplumber

WORDS = set(w.strip().lower() for w in open("/usr/share/dict/words")) if Path("/usr/share/dict/words").exists() else set()

DPI = 300


def word(x):
    """A real word: in the dictionary, and one letter long only if it's "a" or "I"."""
    x = re.sub(r"\W", "", x)
    return (len(x) > 1 or x in ("a", "A", "I")) and x.lower() in WORDS


def norm(s):
    # In an all-caps word (article numbers like "XIIIB"), l, |, 1 and J are misreadings of I.
    s = re.sub(r"\b[A-Z][A-Zl|1J]*[A-Z]\b", lambda m: re.sub(r"[l|1J]", "I", m.group(0)), s)
    s = re.sub(r"[“”„\"]", '"', s)
    s = re.sub(r"[‘’'`]", "'", s)
    s = re.sub(r"[—–‐-]+", "-", s)
    s = s.replace("­", "-")
    return re.sub(r"\s+", "", s)


def render(pdf, d):
    if not list(d.glob("pg-*.png")):
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", str(pdf), str(d / "pg")], check=True)
    return sorted(d.glob("pg-*.png"), key=lambda p: int(re.search(r"pg-(\d+)", p.name).group(1)))


def tesseract(img):
    out = img.with_suffix(".tess.txt")
    if not out.exists():
        subprocess.run(["tesseract", str(img), str(out.with_suffix("").with_suffix("")) + ".tess", "-l", "eng", "--psm", "4"],
                       check=True, capture_output=True)
    return out.read_text()


_rapid = None


def rapid(img):
    global _rapid
    out = img.with_suffix(".rapid.txt")
    if not out.exists():
        if _rapid is None:
            from rapidocr_onnxruntime import RapidOCR
            _rapid = RapidOCR()
        res, _ = _rapid(str(img))
        # Group boxes into printed lines by vertical overlap (a margin label like "(g)" is its own
        # box, slightly offset), then read each line left to right.
        boxes = []
        for box, text, _conf in res or []:
            ys = [pt[1] for pt in box]
            boxes.append((min(ys), max(ys), min(pt[0] for pt in box), text))
        boxes.sort(key=lambda b: (b[0] + b[1]) / 2)
        groups = []
        for top, bot, x, text in boxes:
            g = groups[-1] if groups else None
            if g and min(bot, g["bot"]) - max(top, g["top"]) > 0.5 * min(bot - top, g["bot"] - g["top"]):
                g["items"].append((x, text))
                g["top"], g["bot"] = min(top, g["top"]), max(bot, g["bot"])
            else:
                groups.append({"top": top, "bot": bot, "items": [(x, text)]})
        lines = [(g["top"], " ".join(t for _, t in sorted(g["items"]))) for g in groups]
        out.write_text("\n".join(t for _, t in lines) + "\n")
    return out.read_text()


def layer(pdf, i):
    with pdfplumber.open(pdf) as p:
        return p.pages[i].extract_text() or ""


FURNITURE = re.compile(r"(Page ?[\dIl|]+ ?of ?\d+)", re.I)
LABEL = re.compile(r"^\((?:[a-z]{1,2}|\d{1,3}|[ivx]+|[A-Z])\)[,.;]?$")


def strip_furniture(text):
    """Drop running headers/footers ("The 2026 Billionaire Tax Act ... Page 6 of 32") from a reading."""
    return "\n".join(l for l in text.splitlines() if not FURNITURE.search(l))


def vote_page(t_text, r_text, l_text):
    """Returns (lines, decisions). lines: voted text, keeping T's line breaks."""
    t_text, r_text, l_text = (strip_furniture(x) for x in (t_text, r_text, l_text))
    T = [(w, n) for n, line in enumerate(t_text.splitlines()) for w in line.split()]
    tw = [w for w, _ in T]
    R, L = r_text.split(), l_text.split()
    nt = [norm(w) for w in tw]

    def blocks(other):
        no = [norm(w) for w in other]
        return difflib.SequenceMatcher(None, nt, no, autojunk=False).get_opcodes()

    def segment(ops, other, a1, a2):
        """The stretch of `other` aligned with T[a1:a2] (by the alignment's opcodes)."""
        b1 = b2 = None
        for op, i1, i2, j1, j2 in ops:
            if i2 <= a1 and op != "insert":
                continue
            if i1 >= a2 and not (i1 == i2 == a1):
                break
            if op == "equal":
                lo, hi = max(i1, a1), min(i2, a2)
                if lo < hi:
                    s, e = j1 + (lo - i1), j1 + (hi - i1)
                    b1 = s if b1 is None else min(b1, s)
                    b2 = e if b2 is None else max(b2, e)
            else:
                b1 = j1 if b1 is None else min(b1, j1)
                b2 = j2 if b2 is None else max(b2, j2)
        return other[b1:b2] if b1 is not None else []

    ops_r, ops_l = blocks(R), blocks(L)
    out = list(T)
    decisions, shift = [], 0
    for op, a1, a2, _, _ in ops_r:
        if op == "equal":
            continue
        t_seg = tw[a1:a2]
        r_seg = segment(ops_r, R, a1, a2)
        l_seg = segment(ops_l, L, a1, a2)
        nt_, nr, nl = norm(" ".join(t_seg)), norm(" ".join(r_seg)), norm(" ".join(l_seg))
        if nt_ == nl or nt_ == nr:
            # Same letters. If T ran two words together ("Ifthe") and the agreeing reading splits
            # that token into two dictionary words ("If the"), split it. Nothing else is taken
            # from the other reading (its spacing and quote marks are worse than T's).
            agree = l_seg if nt_ == nl else r_seg
            if len(agree) > len(t_seg):
                fixed, changed = [], False
                for w in t_seg:
                    split = None
                    for j in range(len(agree) - 1):
                        a_, b_ = agree[j], agree[j + 1]
                        if norm(a_ + b_) == norm(w) and all(word(x) for x in (a_, b_)):
                            k = len(re.sub(r"[^\w]", "", a_)) + len(w) - len(w.lstrip("([\"“‘'"))
                            split = [w[:k], w[k:]]
                    fixed += split or [w]
                    changed |= bool(split)
                if changed:
                    line = T[a1][1] if a1 < len(T) else (T[-1][1] if T else 0)
                    new = [(w, line) for w in fixed]
                    out[a1 + shift:a2 + shift] = new
                    shift += len(new) - (a2 - a1)
                    decisions.append(("spacing", " ".join(t_seg), " ".join(fixed)))
            continue
        line = T[a1][1] if a1 < len(T) else (T[-1][1] if T else 0)
        if nr == nl and nr:
            # R and L agree on the letters; take the layer's form, which keeps word spacing
            # (RapidOCR sometimes runs words together: "stategovernment").
            pick = l_seg if len(l_seg) >= len(r_seg) else r_seg
            new = [(w, line) for w in pick]
            out[a1 + shift:a2 + shift] = new
            shift += len(new) - (a2 - a1)
            decisions.append(("replaced", " ".join(t_seg), " ".join(pick)))
        elif t_seg or r_seg or l_seg:
            # All three differ: take the reading closest to the other two (character similarity),
            # if it clearly wins; otherwise T stands. Either way the stretch is logged as unresolved.
            cands = [("T", t_seg), ("R", r_seg), ("L", l_seg)]
            live = [(k, seg) for k, seg in cands if seg]
            sim = lambda a, b: difflib.SequenceMatcher(None, norm(" ".join(a)), norm(" ".join(b))).ratio()
            score = {k: sum(sim(seg, o) for k2, o in live if k2 != k) for k, seg in live}
            best = max(score, key=lambda k: (score[k], k == "T")) if len(live) == 3 else "T"
            # "|" never occurs in legal prose: it's a misread 1, I or l. Prefer a reading without it.
            if "|" in " ".join(t_seg):
                clean = [k for k, seg in live if k != "T" and "|" not in " ".join(seg)]
                if clean:
                    best = "R" if "R" in clean and re.search(r"\d", " ".join(dict(cands)["R"])) else clean[0]
            # A subdivision label like "(j)" is well-formed; "G)" or "!" never is. Don't trade one for the other.
            formed = {k for k, seg in live if len(seg) == 1 and LABEL.match(seg[0])}
            if formed and best not in formed:
                best = "T" if "T" in formed else sorted(formed)[0]
            if best != "T" and (score[best] > score.get("T", 0) + 0.2 or (formed and "T" not in formed)
                                or "|" in " ".join(t_seg)):
                pick = dict(cands)[best]
                new = [(w, line) for w in pick]
                out[a1 + shift:a2 + shift] = new
                shift += len(new) - (a2 - a1)
            else:
                best = "T"
            decisions.append(("unresolved", " ".join(t_seg),
                              f"R: {' '.join(r_seg)!r} / L: {' '.join(l_seg)!r} -> kept {best}"))
    # Roman-numeral article numbers ("XIIIB"): T can read I as J, l, | or 1 and still "agree"
    # under norm(). Write them with I.
    roman = re.compile(r"^([XVIJl|1]*[XV][XVIJl|1]*|[XVI]*[Jl|1][XVI]+)([A-D]?)([,.;:)]*)$")
    for k, (w, n) in enumerate(out):
        m = roman.match(w)
        if m and re.search(r"[Jl|1]", m.group(1)) and re.search(r"[XV]", m.group(1)):
            fixed = re.sub(r"[Jl|1]", "I", m.group(1)) + m.group(2) + m.group(3)
            decisions.append(("roman numeral", w, fixed))
            out[k] = (fixed, n)
    lines = {}
    for w, n in out:
        lines.setdefault(n, []).append(w)
    return [" ".join(lines[n]) for n in sorted(lines)], decisions


def vote(pdf, out_dir):
    """[(page number, [lines], [decisions])] for every page of the PDF."""
    pdf = Path(pdf)
    d = Path(out_dir) / pdf.stem
    d.mkdir(parents=True, exist_ok=True)
    pages = []
    for i, img in enumerate(render(pdf, d)):
        l_text = layer(pdf, i)
        (d / f"pg-{i + 1}.layer.txt").write_text(l_text)
        lines, dec = vote_page(tesseract(img), rapid(img), l_text)
        pages.append((i + 1, lines, dec))
    for img in d.glob("pg-*.png"):
        img.unlink()      # images are re-rendered from the archived PDF on demand; keep the readings
    return pages


if __name__ == "__main__":
    pages = vote(sys.argv[1], sys.argv[2])
    rep = sum(1 for _, _, d in pages for k, *_ in d if k == "replaced")
    unr = [(p, x) for p, _, d in pages for x in d if x[0] == "unresolved"]
    print(f"{len(pages)} pages; {rep} words replaced by majority; {len(unr)} unresolved")
    for p, (_, t, o) in unr:
        print(f"  p{p} T: {t!r}  {o}")
