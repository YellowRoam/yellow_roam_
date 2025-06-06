
# Custom Domain Setup for YellowRoam (yellowroam.com)

This guide explains how to connect your custom domain (`yellowroam.com`) to your deployed YellowRoam app on Render, and ensure it supports HTTPS.

---

## 🛠 Step-by-Step Instructions

### 1. Add Your Domain in Render
1. Go to your **Render Dashboard**
2. Click on your YellowRoam **Web Service**
3. Go to the **Settings** tab
4. Scroll down to **Custom Domains** → Click **Add Custom Domain**
5. Enter: `yellowroam.com` (and optionally `www.yellowroam.com`)
6. Render will generate two DNS records for you to add to your domain provider.

---

### 2. Update DNS Records at Your Registrar
Login to the service where you bought your domain (e.g., GoDaddy, Namecheap) and:

#### Add an A Record:
- **Type**: A  
- **Host/Name**: `@`  
- **Value**: (Render's IP address from the dashboard)  
- **TTL**: Default or 1 hour  

#### Add a CNAME Record:
- **Type**: CNAME  
- **Host/Name**: `www`  
- **Value**: Render's generated domain (e.g., your-app.onrender.com)  
- **TTL**: Default or 1 hour  

---

### 3. Wait for DNS Propagation
- This usually takes 15–30 minutes.
- Render will show a ✅ next to the domain once it's verified.

---

### 4. Enable SSL
Once DNS is verified in Render:
- Toggle **“Automatic HTTPS”** in the Custom Domains section.
- Render will issue a **Let’s Encrypt certificate** automatically.

---

## ✅ Summary
| Task | Status |
|------|--------|
| Add domain to Render | ✅ Required |
| Update DNS with registrar | ✅ Required |
| Wait for Render verification | ✅ Required |
| Enable HTTPS | ✅ Required |
| Test https://yellowroam.com | ✅ Final step |

---

YellowRoam will now be reachable at **https://yellowroam.com** with a valid SSL certificate.

