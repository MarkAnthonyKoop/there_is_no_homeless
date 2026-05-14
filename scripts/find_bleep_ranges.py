"""Extract bleep ranges (start, end) from word-level transcripts.

Uses the JSONs under `transcriptions_word_level/` to find:
  - all occurrences of fuck / fucking / fuckin' / etc.
  - all occurrences of the n-word

Outputs a JSON file mapping clip basename -> list of [start, end] floats.

The render script consumes this to apply a volume=0 envelope at each range.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/home/xx/claude/there_is_no_homeless/transcriptions_word_level")
OUT = ROOT.parent / "bleep_ranges.json"

# Patterns to match. Case-insensitive. Word boundaries on either side.
PATTERNS = {
    "fuck":    re.compile(r"\bfuck", re.IGNORECASE),    # catches fuck, fucks, fucking, fuckin
    "n_word":  re.compile(r"\bnigg", re.IGNORECASE),    # catches nigger, niggers, etc.
}


def _word_iter(seg: dict):
    """Yield (text, start, end) for each word in a segment, with fallback."""
    words = seg.get("words") or []
    if words:
        for w in words:
            t = (w.get("word") or w.get("text") or "").strip()
            s, e = w.get("start"), w.get("end")
            if t and s is not None and e is not None:
                yield t, s, e
    else:
        # No word-level data — fall back to segment-level (less precise).
        yield (seg.get("text") or "").strip(), seg.get("start", 0.0), seg.get("end", 0.0)


def scan(json_path: Path) -> dict:
    data = json.loads(json_path.read_text())
    segments = data.get("segments", [])
    ranges = {kind: [] for kind in PATTERNS}
    for seg in segments:
        for word, s, e in _word_iter(seg):
            for kind, pat in PATTERNS.items():
                if pat.search(word):
                    # Bias the bleep slightly: pad 0.05s each side so the K
                    # sound is fully covered without clipping adjacent vowels.
                    ranges[kind].append([max(0.0, s - 0.05), e + 0.10])
    return ranges


def main() -> None:
    result: dict[str, dict] = {}
    for jf in sorted(ROOT.glob("*.json")):
        clip = jf.stem
        r = scan(jf)
        if any(r.values()):
            result[clip] = r
            print(f"  {clip}:")
            for kind, hits in r.items():
                if hits:
                    print(f"    {kind}: {len(hits)} hit(s)  first={hits[0]}")
    OUT.write_text(json.dumps(result, indent=2))
    print(f"\nwrote -> {OUT}")


if __name__ == "__main__":
    main()
