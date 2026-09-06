# Web Single-Problem Repository Topology

This repository is a concrete single-problem workspace generated from the problem research template that matches its visibility.

The Web GPT + GitHub solution has only two total repository kinds: a problem library and a problem research template. Concrete `problem-<slug>` repositories are the split execution layer. No third total-control repository exists.

The problem library owns discovery, ProblemContract admission, contract digests, and repository locators. This repository owns the admitted problem's Attempt, Route, Obligation, Candidate, verifier receipt, EvidenceLink, Result, and derived Solution view. These truth domains must not be duplicated.

Internal-to-public publication is one-way and allowlist-based. A public repository must not expose private repository locators, source histories, runtime infrastructure, sessions, credentials, or unpublished research artifacts.

Local compute-node and multi-worker orchestration is a separate solution, not a dependency of this Web repository.
