# Minmed Digital Name Cards: mockups

Phone mockups, security explanations and recommended answers, based on Technical Specification draft 0.2 (15/10/2026).

Open `minmed-name-cards.html` in a browser. It is one self-contained file with a tab for each part:

| Tab | Shows |
|---|---|
| Overview | How to read the mockups, the normal Active card, open questions |
| 1 · Not verified | Sign-in or directory failure, new card waiting for approval, change not approved, live check failed |
| 2 · Pending change | A change from Edit my details to approval, including the exact-version rule |
| 3 · Left Minmed | Deactivation when someone leaves Minmed |
| 4 · Security | Every scenario in spec §7, with a CAPTCHA simulator and a token checker |
| 5 · Recommended | A recommended answer to each open question. Highlighted text is recommended wording, not spec |

## Conventions

- On tabs 1 to 4, text inside a phone is either quoted from the spec or a dashed `[placeholder]`.
- Badges mark Proposed, Pending, Candidate, Example only, Not in spec, Sample data and Recommended.
- Light mode only. Brand colours and fonts come from the minmed repo (`frontend/src/index.css`). The "mm" mark is that repo's stand-in mark, not a confirmed logo.
- Alex Tan and every other person shown are fictional. QR codes are not scannable.

## Editing

The file is generated. Edit the files in `src/`, then run:

```
python3 name-card-mockups/src/build.py
```
