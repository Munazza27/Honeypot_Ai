# ⚡ QUICK START GUIDE

## 🎯 What You're Building

An AI agent that:
1. Detects scam messages automatically
2. Pretends to be a victim to keep scammers talking
3. Extracts intelligence (bank accounts, UPI IDs, phone numbers, etc.)
4. Reports findings back to GUVI automatically

## 🚀 Deploy in 5 Minutes

### Step 1: Push to GitHub

```bash
cd honeypot-api

# Initialize git
git init
git add .
git commit -m "Honeypot API for GUVI"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Wait for it to build (2-3 minutes)

### Step 3: Add Environment Variables

In Railway dashboard:
1. Click your service
2. Go to **"Variables"** tab
3. Add:
   - `GROQ_API_KEY` = `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`
   - `YOUR_API_KEY` = `your-secret-api-key-123`
4. Click **"Deploy"**

### Step 4: Generate Public URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. Copy your URL (e.g., `honeypot-api-production.up.railway.app`)

### Step 5: Test It!

```bash
# Test health endpoint
curl https://YOUR_RAILWAY_URL/health

# Test message endpoint
curl -X POST https://YOUR_RAILWAY_URL/api/message \
  -H "x-api-key: your-secret-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked! Verify now!",
      "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {"channel": "SMS", "language": "English", "locale": "IN"}
  }'
```

✅ If you get a response with `"status": "success"` and a reply, you're good!

## 📝 Submit to GUVI

Provide GUVI with:
- **API URL**: `https://YOUR_RAILWAY_URL/api/message`
- **API Key**: `your-secret-api-key-123`

---

## 🔍 How It Works

```
GUVI sends message → Your API detects scam → AI Agent responds → 
Extracts intelligence → After 8-12 messages → Auto-reports to GUVI
```

## 📊 What Gets Extracted

- 💳 Bank account numbers
- 💰 UPI IDs
- 🔗 Phishing links
- 📱 Phone numbers
- 🚨 Suspicious keywords

## ⚙️ Tech Stack

- **AI**: Groq Llama 3.3 70B (fast & smart)
- **Framework**: FastAPI (Python)
- **Deployment**: Railway (free tier works!)
- **Container**: Docker

## 🎓 Key Files

- `main.py` - Main application (scam detection + AI agent)
- `requirements.txt` - Python packages
- `Dockerfile` - Container configuration
- `test_api.py` - Test your API locally
- `DEPLOYMENT.md` - Detailed deployment guide

## 🐛 Common Issues

**Railway build fails?**
- Check you pushed all files including `Dockerfile`
- Verify `requirements.txt` is present

**API returns 401?**
- Make sure you're sending `x-api-key` header
- Check the key matches your environment variable

**No AI response?**
- Verify Groq API key is correct
- Check Railway logs for errors

**Final result not sent?**
- Conversation needs 8+ messages
- Check Railway logs for callback errors

## 📚 Need More Help?

Read `DEPLOYMENT.md` for detailed instructions!

---

**Good luck with the hackathon! 🍀**
