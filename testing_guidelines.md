# 🧪 TESTING_GUIDELINES.md — YellowRoam

This document outlines how to test YellowRoam's MVP features and backend services, as well as how to evaluate prompt behavior, user logic flow, and Stripe subscription handling.

---

## ✅ Core Testing Objectives

1. Ensure prompt input returns dynamic, relevant itinerary information.
2. Validate language selector changes app interface text.
3. Confirm pricing plan buttons trigger correct Stripe checkout session.
4. Verify RoamReach email input sends data (test mode).
5. Test Flask app responds to all defined routes with valid status codes.
6. Ensure environment variables load correctly from `.env`.
7. Confirm Render health check route (`/status`) returns `200 OK`.
8. Check email inputs sanitize and block invalid formats.
9. Validate Stripe test keys trigger no production charges.
10. Ensure app boots with `gunicorn app:app` in production mode.

---

## 🧰 Manual Testing Checklist

| Feature | How to Test | Expected Result |
|--------|-------------|-----------------|
| Prompt | Enter: "What should I do in Cody?" | Returns sample itinerary text |
| Language Switcher | Switch to Spanish | UI text updates |
| Subscribe: Explorer | Click plan | Stripe test checkout screen |
| Email Signup | Enter email → Submit | Logs to console or test inbox |
| Route Check | Visit `/status` | "OK" response |
| Environment | Use `.env.example` → rename `.env` | Flask app boots with keys |
| Stripe | Use test card `4242 4242...` | Checkout completes |
| Gunicorn | Run `gunicorn app:app` | No errors in terminal |
| 404 Handling | Visit invalid route | Returns 404 error |
| CSS Styling | Check page style | Branded fonts/colors display |

---

## 🧪 Prompt Logic Tests

| Input | Expected Pattern |
|-------|------------------|
| "Where should I go in Gardiner?" | Suggest hikes + eats |
| "How do I get to Old Faithful?" | Show route + elevation |
| "What’s the best time to visit?" | Returns seasonal info |
| "Do I need a bear spray?" | Gives safety tips |
| "Can I see moose in Lamar?" | Wildlife info returns |

---

## 🛡️ Edge Case Testing

1. Empty prompt → graceful error or fallback
2. Extremely long input → avoid crash
3. Nonsensical prompt → safe, filtered response
4. Double-clicking plan buttons → no Stripe duplication
5. Invalid emails → blocked with error
6. Language set to unsupported option → defaults to English
7. `/status` spammed rapidly → no crash
8. Render env vars missing → visible error or fallback
9. Concurrent prompt inputs → response time is acceptable
10. High-traffic load simulation → app remains responsive

---

## 🔁 Automation Ready (Future)

- Prompt classification tests via Pytest
- Email input format tests
- Route response speed <500ms
- Prompt vs. response relevance testing

---

## 🧾 Pre-Launch Final Tests

- [ ] Prompt box renders and submits
- [ ] Plans render & connect to Stripe
- [ ] Language dropdown is selectable
- [ ] Email form logs correctly
- [ ] `.env` loaded without error
- [ ] App boots in local + Render environments

---

## 📬 Reporting Issues

Contact: **heyday6159@gmail.com** with subject “Bug Report: YellowRoam”

---

*File auto-generated and reviewed for early-stage QA and investor-readiness.*