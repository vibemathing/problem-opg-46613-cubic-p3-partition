"""Candidate-side replay of the exact cover; this file asserts no execution.

Input is the TSV output of factor_cover12.cpp. Run under an external time and
memory limit as well as the internal deadline. Successful replay is not a
registered mathematical-verifier receipt or a root admission.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
import time
from pathlib import Path
from typing import Iterator

N = 12
TYPES = ((4, 8), (5, 7), (3, 4, 5), (4, 4, 4))
HEADER = "# opg46613-bad-factor-cover-v1"
MAX_BYTES = 2 * 1024 * 1024
MAX_ROWS = 4 * 10395
DELETIONS = ((),) + tuple((u,) for u in range(N)) + tuple(itertools.combinations(range(N), 2))
MATCHING = re.compile(r"[0-9ab]{12}\Z")
COUNT_PAIR = re.compile(r"([0-9]{1,5}):([0-9]{1,5})\Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def decode(text: str) -> tuple[int, ...]:
    require(MATCHING.fullmatch(text) is not None, "matching must be twelve lowercase base-12 digits")
    mate = tuple(int(c, 16) for c in text)
    require(all(mate[u] != u and mate[mate[u]] == u for u in range(N)), "matching is not a fixed-point-free involution")
    return mate


def encode(mate: tuple[int, ...]) -> str:
    return "".join("0123456789ab"[v] for v in mate)


def cycle_factor(kind: int) -> tuple[frozenset[int], ...]:
    neighbors: list[set[int]] = [set() for _ in range(N)]
    start = 0
    for length in TYPES[kind]:
        for i in range(length):
            u, v = start + i, start + (i + 1) % length
            neighbors[u].add(v)
            neighbors[v].add(u)
        start += length
    require(start == N and all(len(a) == 2 for a in neighbors), "bad fixed factor")
    return tuple(frozenset(a) for a in neighbors)


def union_graph(factor: tuple[frozenset[int], ...], mate: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    require(all(mate[u] not in factor[u] for u in range(N)), "input matching overlaps its fixed factor")
    graph = tuple(factor[u] | {mate[u]} for u in range(N))
    require(all(len(a) == 3 for a in graph), "union is not cubic")
    return graph


def three_connected(graph: tuple[frozenset[int], ...]) -> bool:
    for deleted in DELETIONS:
        remaining = set(range(N)).difference(deleted)
        root = min(remaining)
        seen, stack = {root}, [root]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v in remaining and v not in seen:
                    seen.add(v)
                    stack.append(v)
        if seen != remaining:
            return False
    return True


def check_witness(graph: tuple[frozenset[int], ...], mate: tuple[int, ...]) -> tuple[int, ...]:
    require(all(mate[u] in graph[u] for u in range(N)), "witness contains a nonedge")
    # Use connected-component sizes, rather than the generator's cycle walk.
    complement = tuple(graph[u].difference((mate[u],)) for u in range(N))
    require(all(len(a) == 2 for a in complement), "complement is not two-regular")
    remaining, sizes = set(range(N)), []
    while remaining:
        root = min(remaining)
        remaining.remove(root)
        stack, size = [root], 0
        while stack:
            u = stack.pop()
            size += 1
            for v in complement[u]:
                if v in remaining:
                    remaining.remove(v)
                    stack.append(v)
        require(size >= 3 and size % 3 == 0, "witness has a nondivisible component")
        sizes.append(size)
    return tuple(sorted(sizes))


def run(certificate: Path, seconds: float) -> dict[str, object]:
    require(0 < seconds <= 1800, "invalid internal time budget")
    deadline = time.monotonic() + seconds
    ticks = 0

    def tick() -> None:
        nonlocal ticks
        ticks += 1
        if ticks % 256 == 0:
            require(time.monotonic() < deadline, "deadline: replay is incomplete")

    with certificate.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    require(len(data) <= MAX_BYTES, "certificate exceeds the two-MiB budget")
    text = data.decode("ascii", errors="strict")
    require(text.endswith("\n"), "certificate lacks final newline")
    lines = text.splitlines()
    require(2 <= len(lines) <= MAX_ROWS + 2, "invalid certificate row count")
    require(lines[0] == HEADER, "wrong certificate version")
    footer = lines[-1].split("\t")
    require(len(footer) == 5 and footer[0] == "# DONE", "missing complete-run marker")
    declared: list[tuple[int, int]] = []
    for field in footer[1:]:
        match = COUNT_PAIR.fullmatch(field)
        require(match is not None, "invalid footer count")
        assert match is not None
        count, kept = int(match.group(1)), int(match.group(2))
        require(0 <= kept <= count <= 10395, "footer count exceeds proved matching bound")
        declared.append((count, kept))

    factors = tuple(cycle_factor(t) for t in range(4))
    supplied: dict[tuple[int, str], str] = {}
    spectra: dict[str, int] = {}
    for number, line in enumerate(lines[1:-1], start=2):
        tick()
        fields = line.split("\t")
        require(len(fields) == 3 and fields[0] in ("0", "1", "2", "3"), f"malformed row {number}")
        kind, input_code, witness_code = int(fields[0]), fields[1], fields[2]
        key = (kind, input_code)
        require(key not in supplied, "duplicate input key")
        original, witness = decode(input_code), decode(witness_code)
        graph = union_graph(factors[kind], original)
        require(three_connected(graph), "row represents a graph outside the retained domain")
        lengths = check_witness(graph, witness)
        supplied[key] = witness_code
        spectrum_key = ",".join(str(n) for n in lengths)
        spectra[spectrum_key] = spectra.get(spectrum_key, 0) + 1

    def all_inputs(factor: tuple[frozenset[int], ...]) -> Iterator[tuple[int, ...]]:
        mate = [-1] * N

        def visit(remaining: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
            tick()
            if not remaining:
                yield tuple(mate)
                return
            u = remaining[0]
            for v in remaining[1:]:
                if v in factor[u]:
                    continue
                mate[u], mate[v] = v, u
                yield from visit(tuple(w for w in remaining if w != u and w != v))
                mate[u], mate[v] = -1, -1

        yield from visit(tuple(range(N)))

    actual: list[tuple[int, int]] = []
    for kind, factor in enumerate(factors):
        count = kept = 0
        for original in all_inputs(factor):
            count += 1
            require(count <= 10395, "input generation exceeded its proved bound")
            graph = union_graph(factor, original)
            if not three_connected(graph):
                continue
            kept += 1
            key = (kind, encode(original))
            require(key in supplied, "certificate omits a retained matching/cycle union")
            del supplied[key]
        actual.append((count, kept))
    require(not supplied, "certificate includes an ungenerated input key")
    require(actual == declared, "footer counts disagree with complete regeneration")
    require(time.monotonic() < deadline, "deadline: replay is incomplete")
    return {
        "verdict": "candidate_only",
        "certificate_sha256": hashlib.sha256(data).hexdigest(),
        "coverage_scheme": "four fixed bad factors and all disjoint perfect matchings",
        "certificate_complete": True,
        "counts_by_type": [{"cycle_lengths": list(TYPES[t]), "unions": a, "retained": b}
                           for t, (a, b) in enumerate(actual)],
        "selected_witness_spectra": spectra,
        "limitations": ["candidate-side replay, not an admitted verifier receipt",
                        "the lower-order implication also uses the accompanying finite-cover proof",
                        "counts include repeated graph isomorphism classes"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--seconds", type=float, default=120.0)
    args = parser.parse_args()
    try:
        report = run(args.certificate, args.seconds)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"BLOCK: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
