# Cycle-gluing transport reconciliation

Verdict: candidate_only. Research remains NONTERMINAL.
Base: 0f009927bfffa44335148cb65ae93596288b50c4. Existing branch reused.

All eight previously delivered source blobs and all five original proof/request/
manifest blobs retain their original bytes. The original archive is preserved
losslessly in thirteen ordered UTF-8 segments. Run, from this directory:

    python3 -I -S restore_archive.py
    python3 -I -S decode_data.py

The first command reconstructs exactly 24652 bytes with SHA-256
bb288e3c419fc26f63cd71fb610ba05f0ef23e5380c1ac4bc8cead7de4618669.
The second verifies and restores the 21 original members, totalling 95730 bytes.
Neither operation is a new mathematical replay. Existing different files are
not overwritten. Both commands use the existing byte identities, not new
invented execution receipts.

The old manifest.json is retained as the original prepared-material manifest.
Its reference to fourteen physical candidate files is superseded for transport:
replay-data.json is a restored member, represented in Git by the thirteen parts.
The final packet enumerates the actual committed paths and SHA-256 values.
The old verifier request's archive fingerprint applies to the reconstructed
bytes; its replay order must start with restore_archive.py before decode_data.py.

Long-content copy attempts produced wrong byte identities; they were not
accepted as archived output. The final tree excludes the malformed part-04.txt
and uses only blobs matching the frozen segment identities. Intermediate branch
history is retained without force. The malformed whole-archive dangling blob
was never attached to a candidate tree. No old receipt is replaced by a new one.

No proof, computation claim, original source, or prior main artifact is changed.
No missing historical material from earlier candidates is claimed recovered.
This transaction completes storage of this cycle-gluing package only. The first
open root lemma is still selection of a feasible matching subset for arbitrary
cycle count, not the finite byte-restoration task.
