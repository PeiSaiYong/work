# Minmed Digital Name Cards: mockups

Phone mockups and security explanations based on Technical Specification draft 0.2 (15/10/2026).

Open `index.html` in a browser. Each page works on its own (CSS and JS are inlined).

| File | Shows |
|---|---|
| `index.html` | How to read the mockups, the normal Active card, open questions |
| `1-not-verified.html` | Sign-in or directory failure, new card waiting for approval, change not approved, live check failed |
| `2-pending-change.html` | A change from Edit my details to approval, including the exact-version rule |
| `3-left-minmed.html` | Deactivation when someone leaves Minmed |
| `4-security.html` | Every scenario in spec §7, with a CAPTCHA simulator and a token checker |

## Conventions

- Text inside a phone is either quoted from the spec or a dashed `[placeholder]`. No UI wording was invented.
- Badges mark Proposed, Pending, Candidate, Example only, Not in spec and Sample data.
- Brand colours and fonts come from the minmed repo (`frontend/src/index.css`). The "mm" mark is that repo's stand-in mark, not a confirmed logo.
- Alex Tan and every other person shown are fictional. QR codes are not scannable.

## Editing

The pages are generated. Edit the files in `src/`, then run:

```
python3 name-card-mockups/src/build.py
```
