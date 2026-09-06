"""Expand a bounded rank certificate to the exact TSV used by the cover checker.

This is candidate-side certificate transport, not a registered verifier.
The sibling check_factor_cover12.py supplies only finite graph primitives.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import itertools
import json
import time
import zlib
from pathlib import Path
from check_factor_cover12 import N, HEADER, cycle_factor, union_graph, three_connected, encode

MAX_RANKS = 41580
MAX_INPUT_BYTES = 16384


def expand(source: Path, destination: Path, seconds: float) -> dict[str, object]:
    if not 0 < seconds <= 120:
        raise ValueError("invalid time limit")
    deadline = time.monotonic() + seconds
    data = source.read_bytes()
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError("rank certificate exceeds input budget")
    packet = json.loads(data)
    if packet.get("format") != "opg46613-factor-cover-ranks-v1":
        raise ValueError("wrong certificate format")
    raw = base64.b64decode(packet["ranks_zlib_base64"], validate=True)
    inflater = zlib.decompressobj()
    ranks = inflater.decompress(raw, MAX_RANKS + 1)
    if len(ranks) > MAX_RANKS or not inflater.eof or inflater.unused_data or inflater.unconsumed_tail:
        raise ValueError("invalid or oversized compressed ranks")
    if len(ranks) != packet["rank_count"] or hashlib.sha256(ranks).hexdigest() != packet["ranks_sha256"]:
        raise ValueError("rank length/digest mismatch")
    if any(rank > 5 for rank in ranks):
        raise ValueError("rank outside this certificate's declared range")
    ticks = 0

    def matchings(allowed, remaining=tuple(range(N)), mate=None):
        nonlocal ticks
        ticks += 1
        if ticks % 128 == 0 and time.monotonic() >= deadline:
            raise ValueError("deadline: expansion incomplete")
        if mate is None:
            mate = [-1] * N
        if not remaining:
            yield tuple(mate)
            return
        u = remaining[0]
        for v in remaining[1:]:
            if v in allowed[u]:
                mate[u], mate[v] = v, u
                yield from matchings(allowed, tuple(w for w in remaining if w not in (u, v)), mate)

    lines = [HEADER]
    position = 0
    counts = []
    for kind in range(4):
        factor = cycle_factor(kind)
        allowed = tuple(frozenset(range(N)) - factor[u] - {u} for u in range(N))
        count = kept = 0
        for original in matchings(allowed):
            count += 1
            graph = union_graph(factor, original)
            if not three_connected(graph):
                continue
            kept += 1
            if position >= len(ranks):
                raise ValueError("missing rank")
            rank = ranks[position]
            position += 1
            witness = next(itertools.islice(matchings(graph), rank, rank + 1), None)
            if witness is None:
                raise ValueError("rank does not select a perfect matching")
            lines.append(f"{kind}\t{encode(original)}\t{encode(witness)}")
        counts.append((count, kept))
    if position != len(ranks):
        raise ValueError("unused ranks")
    lines.append("# DONE" + "".join(f"\t{count}:{kept}" for count, kept in counts))
    output = ("\n".join(lines) + "\n").encode("ascii")
    digest = hashlib.sha256(output).hexdigest()
    if digest != packet["expanded_tsv_sha256"] or len(output) != packet["expanded_tsv_bytes"]:
        raise ValueError("expanded TSV length/digest mismatch")
    if time.monotonic() >= deadline:
        raise ValueError("deadline: expansion incomplete")
    # Do not overwrite a pre-existing output, even after successful expansion.
    with destination.open("xb") as stream:
        stream.write(output)
    return {"verdict": "candidate_only", "rows": position, "expanded_tsv_sha256": digest,
            "next_step": "Run check_factor_cover12.py on the expanded TSV; expansion alone is not a witness check."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rank_certificate", type=Path)
    parser.add_argument("output_tsv", type=Path)
    parser.add_argument("--seconds", type=float, default=30)
    args = parser.parse_args()
    try:
        print(json.dumps(expand(args.rank_certificate, args.output_tsv, args.seconds), sort_keys=True, indent=2))
    except (OSError, ValueError, KeyError, TypeError, zlib.error) as error:
        print(f"BLOCK: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
