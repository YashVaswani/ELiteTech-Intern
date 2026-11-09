# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue. Instead, email the maintainer listed in the repository's contact information, or open a [GitHub private security advisory](https://docs.github.com/en/code-security/security-advisories) if the repo is hosted on GitHub.

Please include:

- A description of the vulnerability and its impact
- Steps to reproduce
- Any suggested remediation

We aim to acknowledge reports within 5 business days.

## Supported Versions

Only the `main` branch is actively maintained and receives security fixes.

## Known Security Considerations

- Authentication uses JWT bearer tokens (HS256). Rotate `SECRET_KEY` before any production deployment and never commit it.
- Uploaded images are validated by content type and size (`MAX_UPLOAD_MB`) but are not scanned for malware — do not deploy this as a public, unauthenticated upload endpoint without additional hardening (rate limiting, antivirus scanning, storage isolation).
- Passwords are hashed with bcrypt via `passlib`; never log or store plaintext passwords.
- CORS origins are restricted via `CORS_ORIGINS` — update this for your deployed frontend domain and avoid `*` in production.
