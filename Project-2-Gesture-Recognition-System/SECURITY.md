# Security Policy

## Supported Versions

This project is pre-1.0. Only the `main` branch receives security fixes.

## Reporting a Vulnerability

Please **do not** open a public issue for security vulnerabilities.

Instead, open a [GitHub Security Advisory](../../security/advisories/new) on
this repository (Security tab → "Report a vulnerability"), or email the
maintainer listed in `README.md`. Include:

- A description of the vulnerability and its impact
- Steps to reproduce (a minimal repro is ideal)
- Any known mitigations

You should receive an acknowledgement within a few days. We'll work with you
to confirm the issue, prepare a fix, and coordinate disclosure timing.

## Scope notes

- This app processes camera/image frames **in memory only** — no gesture
  images or video are persisted to disk or a database by default.
- The WebSocket prediction endpoint does not require authentication out of
  the box; if you deploy this publicly, put it behind your own auth/rate
  limiting (see `README.md` → Deployment).
