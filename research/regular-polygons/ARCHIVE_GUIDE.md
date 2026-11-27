# Source inventory and supplement

The 76 records in [SOURCE_INVENTORY.tsv](SOURCE_INVENTORY.tsv) refer to original files, not necessarily tracked Git blobs. The location classes mean:

- `existing`: a file with matching digest in the previous repository SHA256SUMS (possibly stored in split transport form).
- `nested`: byte-preserved within the 22:00 cumulative ZIP (including its nested histories).
- `supplement`: a separate source file in the locally assembled supplement; these binaries were not uploaded by the documentation commit.

The supplement is `Math-regular-polygons-research-supplement-2026-11-27.zip`, 192161562 bytes, SHA-256 `1a8fd9d97f703521329651e54696b60ea730d3042117bea5affda47182a9f744`. Its internal `artifacts/research-snapshots/INDEX.tsv` records full paths and nested provenance. There are 45 directly supplied source files, 23 nested sources and 8 sources already identified by the historical repository manifest. No original binary has been silently replaced.

Extract the supplement into a separate directory, inspect the index, and copy the `artifacts/research-snapshots/` directory into the repository. Each original file is below the GitHub per-file limit; do not add the outer supplement ZIP itself to Git. Verify the latest archive with the repository's `code/verify_capacity_snapshot.py` before staging. Do not overwrite unrelated work or alter the old artifact manifest. The mathematical replay instructions are in [EVIDENCE_AND_REPLAY.md](EVIDENCE_AND_REPLAY.md).

Source bytes and proof validity are different. A complete upload of the supplement is still required for offline reproduction of the latest proofs from a clean clone.
