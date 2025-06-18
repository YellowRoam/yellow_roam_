
# 🧪 YellowRoam Testing Guidelines

Welcome to the YellowRoam testing guide. This document provides a clear overview of how to test core app functionality across multilingual support, fallback logic, and PWA installability. Use these steps during development, QA, or release validation.

---

## 🔁 API Endpoint Testing

### Chat Endpoint

**Route:** `POST /api/chat`  
**Payload:**

```json
{
  "message": "Where can I see wolves in Yellowstone?",
  "lang": "en"
}
```

**Expected Response:**
- A JSON object with a `response` key containing a valid string.

---

## 🌐 Multilingual Prompt Testing

### Supported Languages
- English (`en`)
- Spanish (`es`)
- French (`fr`)
- Hindi (`hi`) *(optional — remove if file missing)*

### How to Test:
1. Open your frontend.
2. Select a language from the dropdown (e.g., Español).
3. Enter a question like:  
   - **Spanish:** `¿Dónde puedo ver lobos en Yellowstone?`
   - **French:** `Où puis-je voir des loups dans le parc de Yellowstone ?`
4. Click "Ask YellowRoam".
5. **Expected:** Response appears in the selected language using the correct logic file.

---

## 🛑 Fallback Logic Testing

### What to Test
- Typos
- Unrecognized questions
- Partial matches

### Example Prompts:
- `wherre do i see wolvs?`
- `yellowstoon animls`
- `qwerty`

### Expected Behavior:
- YellowRoam should return a fallback response (e.g., “I’m not sure how to answer that yet...”) instead of crashing or returning an error.

---

## 📲 PWA Install & Service Worker Tests

### Manifest Location
- Ensure `<link rel="manifest" href="/static/manifest.json">` is in your `<head>`

### Service Worker Registration
- Should appear in browser dev tools under:
  - `Application` tab → `Service Workers`

### How to Verify:
1. Load your frontend.
2. Open dev tools (`Cmd+Opt+I` or `F12`)
3. Go to `Application > Manifest` and confirm:
   - App name, icon, start_url, display = `standalone`
4. Go to `Application > Service Workers` and confirm:
   - Status: `activated and running`
   - Scope is `/`

---

## ⚠️ Known Issues / Edge Cases

- Missing `.logic.json` files will show "Skipping missing file" warnings.
- Hindi logic must be present if `hi` is in dropdown.
- OpenAI API errors will throw 500 unless caught in fallback.

---

## ✅ Final QA Checklist

- [ ] English prompt works
- [ ] Spanish and French prompt responses render correctly
- [ ] Fallback triggers for nonsense input
- [ ] App is installable on Chrome and Safari
- [ ] Manifest and Service Worker load without error
- [ ] App works offline (after first visit) with cached shell

---

For questions or contributions, please contact the YellowRoam development team.
