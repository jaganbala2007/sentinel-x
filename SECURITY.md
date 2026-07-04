# Security Policy — Sentinel-X

## Supported Versions

| Version | Status          | Security Updates |
|---------|-----------------|-----------------|
| 1.0.x   | ✅ Active        | Yes             |
| 0.2.x   | ⚠️ Deprecated   | Critical only   |
| < 0.2   | ❌ Unsupported  | No              |

---

## Reporting a Vulnerability

**⚠️ Please do NOT open a public GitHub issue for security vulnerabilities.**

Sentinel-X is designed for industrial safety-critical environments. A security vulnerability in this system could, in a production deployment, impact real machinery and worker safety. We take security reports extremely seriously.

### How to Report

**Option 1 — GitHub Private Security Advisory (Preferred)**

Use GitHub's built-in private reporting:
1. Navigate to the [Security tab](https://github.com/jaganbala2007/sentinel-x/security)
2. Click **"Report a vulnerability"**
3. Fill out the advisory form with full details

**Option 2 — Direct Email**

Send a detailed report to: **jaganbala2007@gmail.com**

Use the subject line: `[SENTINEL-X SECURITY] <brief description>`

Encrypt your message using our PGP key if sending sensitive details.

---

## What to Include in Your Report

Please provide as much of the following as possible:

- **Description** — What is the vulnerability and what could it be exploited for?
- **Affected component** — Frontend, Backend API, Docker config, CI pipeline?
- **Steps to reproduce** — Exact steps that trigger the issue
- **Proof of concept** — Code snippet or screenshot if applicable
- **Impact assessment** — What could an attacker achieve?
- **Suggested fix** — If you have one

---

## Response Timeline

| Stage | Timeline |
|---|---|
| Acknowledgment of receipt | Within **48 hours** |
| Initial assessment | Within **5 business days** |
| Fix developed | Within **14 days** (critical), **30 days** (high) |
| Public disclosure | After patch is released and verified |

---

## Scope — What We Care About

**In scope:**
- Authentication bypass in the auth gate
- API endpoint authorization failures
- Secret/credential exposure in code or CI logs
- Docker image vulnerabilities (high or critical CVEs)
- Injection vulnerabilities (SQL, command, script)
- WebSocket stream hijacking
- Dependency vulnerabilities in `requirements.txt`

**Out of scope:**
- Client-side simulation UI bugs (not security-critical)
- Issues requiring physical access to hardware
- Social engineering attacks
- Denial-of-service via network flooding

---

## Security Best Practices for Deployers

If you are deploying Sentinel-X in a production environment:

1. **Change all default credentials** — Never use demo passwords in production
2. **Use environment variables** — Never hardcode secrets; use `.env` files or secret managers
3. **Enable TLS/HTTPS** — All API and WebSocket traffic must be encrypted
4. **Firewall the PLC network** — The Modbus/TCP interface must be on an isolated VLAN
5. **Rotate JWT keys regularly** — Use strong `SECRET_KEY` values (`openssl rand -hex 32`)
6. **Keep dependencies updated** — Run `pip-audit` regularly against `requirements.txt`
7. **Enable PostgreSQL SSL** — Use `?sslmode=require` in `DATABASE_URL`
8. **Restrict MQTT access** — Use ACL lists in Mosquitto to limit topic access per device

---

## Acknowledgements

We thank security researchers who responsibly disclose vulnerabilities. Contributors who find significant issues will be acknowledged in our `CHANGELOG.md` (with their permission).

---

*Security is not a feature — it's a foundation. Thank you for helping keep Sentinel-X safe.*
