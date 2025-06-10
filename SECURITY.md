# 🔐 Security Policy — YellowRoam

YellowRoam is committed to providing a safe and privacy-respecting experience for all users and travelers. This document outlines our current security standards, data protection practices, and contribution guidelines.

---

## ✅ Supported Versions

| Version | Supported |
|---------|-----------|
| MVP (current build) | ✅ Yes |
| Future feature builds | ⏳ Pending security audit |

---

## 🔒 Key Security Practices

1. `.env` is used to store all sensitive keys (Stripe, domain, Flask secret).
2. `.env` is never committed to Git or exposed publicly.
3. Rate limiting is in place to prevent abuse of routes (via Flask logic or proxy rules).
4. All endpoints are monitored via `/status` health checks.
5. Stripe logic operates in test mode by default until switched in production.
6. All redirects use HTTP 303 for safe browser handling.
7. Prompt and email form data is sanitized and validated.
8. Logging avoids sensitive or user-identifying data.
9. Secure deployment via Render.com with proper environment settings.
10. HTTPS is enforced in production via platform setup.

---

## 🚨 Reporting a Vulnerability

If you discover a vulnerability or security concern, please email:

📩 **heyday6159@gmail.com**

We aim to respond within 24–48 hours.

---

## 🧰 Deployment Hygiene

- `.gitignore` ensures `.env`, log files, system cache, DBs are excluded.
- Stripe webhooks (when added) must validate secret signature headers.
- Admin access should be rate-limited and protected in future versions.

---

## 📉 Rate-Limiting Policy

YellowRoam enforces a usage limit to protect against overload:

- `/prompt`: Max 25 requests per IP/hour (planned)
- `/signup`: Max 10 requests per IP/hour (planned)
- `/subscribe/<plan>`: Redirect only, no repeated session creation

A more advanced backend gateway may be implemented in future builds.

---

## 🛑 Do Not Commit

Never commit the following:
- `app.py` with hardcoded secrets
- `.env` files
- Raw Stripe keys
- Access logs

---

## 🧪 Testing Before Launch

Every deployment is reviewed against the following:
- Flask logic integrity
- Gunicorn startup compatibility
- Stripe error fallbacks
- Environment variable loading
- Prompt injection or malformed input handling

---

## 📄 Document History

- Version 1.0 created during MVP launch window
- Last updated: JUNE 2025

---

*This file was auto-generated and verified against YellowRoam system security standards.*