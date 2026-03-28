# Research Note

## Work Packet

- Packet: `WP-001`
- Run: `RUN-20260328-221704`
- Bundle: `team/reports/WP-001-bundle.yaml`
- Author: `codex`
- Date: `2026-03-29`

## Question

- What security-sensitive constraints should shape the first milestone of a local CLI expense split calculator that accepts command-line and JSON input?

## Findings

- Monetary values should use `decimal.Decimal`, not binary `float`, because the Python standard library documents exact decimal arithmetic and explicit rounding control for financial-style calculations.
- Input validation should be allowlist-first at both syntactic and semantic levels. For this repo that means strict participant name rules, bounded participant counts, non-negative amount parsing, and explicit rejection of malformed or duplicate entries.
- JSON input should be treated as untrusted even in a local CLI. Python documents that malicious JSON may consume excessive CPU or memory, so file size and payload size should be bounded before parsing.
- File handling should stay narrow: accept only explicit local files, reject missing paths and non-regular files, and avoid any design that follows user-controlled output locations in the first milestone.
- The core arithmetic invariant should be explicit: after normalization and rounding, total credits and total debts must net to zero, and any remainder policy must be deterministic and documented.

## Sources

- Python `decimal` documentation: https://docs.python.org/3.11/library/decimal.html
- Python `json` documentation: https://docs.python.org/3/library/json.html
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

## Implications

- The implementation milestone should parse money from strings into `Decimal` and quantize with one documented rounding rule.
- The design milestone should specify validation rules for participant identifiers, payment amounts, duplicate names, empty groups, and oversized JSON payloads.
- Verification should include arithmetic invariants, malformed JSON rejection, duplicate participant handling, and deterministic rounding tests.
- The README should document the accepted input shapes and the exact rounding policy before implementation is considered complete.

## Unknowns

- Which rounding rule should be the default for settlement output: `ROUND_HALF_UP`, `ROUND_HALF_EVEN`, or a stricter exact-cent-only policy?
- What participant-count ceiling is acceptable for the first milestone without overengineering the CLI?
- Whether the implementation should reject or normalize repeated participant names in file input is still a design decision for `WP-002`.
