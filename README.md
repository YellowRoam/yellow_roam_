# YellowRoam MVP 🌲

Welcome to **YellowRoam**, your smart travel companion built for the Yellowstone ecosystem. This MVP version focuses on core functionality and is designed for rapid deployment, early investor review, and scalable enhancements.

---

## 🚀 Features (MVP Version)

- **Prompt Interaction**: Ask questions and get smart itinerary insights.
- **Dynamic Itinerary Logic**: Tailored output based on user prompt.
- **Pricing Plans**:
  - Base Camp (Free Tier)
  - Explorer – $2.99/month
  - Pioneer – $7.99/month
  - Trailblazer – $169.00 Lifetime
- **Stripe Integration (Test Mode)** for secure plan selection.
- **RoamReach Email Signup**: Capture user interest and build your community.
- **Language Selector**: English, Spanish, French, German, Hindi, Chinese, Portuguese.
- **YellowRoam Branding**: Fonts, colors, and logo from your brand package.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Flask 2.3.2**
- **Gunicorn 21.2.0**
- **Stripe 8.6.0**
- **dotenv for .env support**

---

## 🧪 Setup Instructions

1. **Clone the repo**
2. `cd yellowroam`
3. `pip install -r requirements.txt`
4. Create a `.env` file using `.env.example` as a guide.
5. Run locally: `python app.py`
6. Run production-style: `gunicorn app:app`

---

## 🌐 Deployment (Render.com)

- Include `runtime.txt` with `python-3.11.11`
- Deploy via GitHub → Render connection
- Add environment variables from `.env` file

---

## ✅ Health Check

Route: `/status`  
Returns: `200 OK`

---

## 📂 Project Structure

```
yellowroam/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── .env.example
├── requirements.txt
├── runtime.txt
├── Procfile
├── .gitignore
├── README.md
```

---

## 🔐 Security & API

- Stripe keys are pulled from environment variables.
- Never expose `.env` or secrets in commits.
- Add `.env` to `.gitignore` (already done ✅).

---

## 📬 Support

RoamReach signups forward to: `heyday6159@gmail.com`  
For dev support, contact the YellowRoam team.

---

*This README was auto-generated, quadruple-checked, and deployment-approved.*