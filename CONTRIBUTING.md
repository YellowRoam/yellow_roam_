# 🤝 CONTRIBUTING.md — YellowRoam

Welcome to the YellowRoam project! This document outlines the process for proposing changes, reporting bugs, and collaborating on improvements — while keeping our codebase secure, maintainable, and legally protected.

---

## 🚫 Outside Contributions

YellowRoam is not currently accepting public pull requests or outside contributors. All development is done internally or through approved collaborators under NDA.

---

## ✅ Who Can Contribute?

Only the following may contribute:
- Internal developers
- Contracted AI or backend specialists
- Approved collaborators with signed agreement
- App owner (Andy Boyd)

---

## 🔒 Important Rules

1. **Do not share source code** externally without written permission.
2. **Do not reuse code** from YellowRoam in other projects.
3. All contributions must be original or licensed for internal commercial use.
4. Include all changes in a local Git branch before proposing merges.
5. Do not commit `.env`, Stripe secrets, or user email data.

---

## 🛠️ Suggested Internal Contribution Workflow

1. Clone the YellowRoam repo locally
2. Create a branch: `feature/<feature-name>` or `fix/<bug-name>`
3. Work locally and commit often with clear messages
4. Test using manual QA checklist and `/status` route
5. When ready, push your branch and notify project lead

---

## 🧪 Internal Testing Expectations

- Use `testing_guidelines.md` before submitting changes
- Test all prompt logic
- Verify no broken routes or unhandled exceptions
- Confirm Stripe flows return valid test sessions
- Ensure `.env` is correctly loaded and not committed

---

## 📦 File Structure Conventions

- `/static/` → Stylesheets, branding, logos
- `/templates/` → HTML front-end
- `app.py` → Flask core
- `.env` → Sensitive keys (never committed)
- `Procfile`, `runtime.txt` → Deployment control

---

## 🔁 Version Control

- Use semantic commit messages: `feat:`, `fix:`, `docs:`, `refactor:`
- Always work in feature branches
- Coordinate merges via project lead

---

## 📧 Questions?

If you are part of the project team and need clarification:

Contact: **heyday6159@gmail.com**

---

*This document is version-controlled and reviewed during every major feature release.*