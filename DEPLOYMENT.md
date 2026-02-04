# 🚀 DEPLOYMENT GUIDE - Agentic Honey-Pot API

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Testing](#local-testing)
3. [Railway Deployment](#railway-deployment)
4. [Testing Your Deployed API](#testing-your-deployed-api)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- ✅ Groq API Account (you already have the key)
- ✅ Railway Account (sign up at https://railway.app)
- ✅ GitHub Account (optional, but recommended)

### Your Keys
- **Groq API Key**: `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`
- **Your API Key**: `your-secret-api-key-123` (you can change this to anything)

---

## Local Testing

### Step 1: Install Dependencies

```bash
# Make sure you're in the project directory
cd honeypot-api

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Run Locally

```bash
# Run the application
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Test Locally

Open a new terminal and run:

```bash
python test_api.py
```

This will test:
- Health check endpoint
- Single message processing
- Full scam conversation flow

---

## Railway Deployment

### Method 1: Using Railway Dashboard (Easiest)

#### Step 1: Create GitHub Repository

1. Go to GitHub and create a new repository (e.g., "honeypot-scam-detection")
2. Initialize with README (optional)

#### Step 2: Push Your Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Agentic Honey-Pot API"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Step 3: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select your honeypot repository
6. Railway will detect the Dockerfile and start building

#### Step 4: Set Environment Variables

1. In your Railway project dashboard, click on your service
2. Go to "Variables" tab
3. Add these variables:
   - `GROQ_API_KEY`: `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`
   - `YOUR_API_KEY`: `your-secret-api-key-123` (or your custom key)

4. Click "Deploy" to redeploy with environment variables

#### Step 5: Get Your Public URL

1. Go to "Settings" tab
2. Scroll to "Networking"
3. Click "Generate Domain"
4. Copy your public URL (e.g., `honeypot-api-production.up.railway.app`)

### Method 2: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project in your directory
cd honeypot-api
railway init

# Link to a new project or existing one
railway link

# Set environment variables
railway variables set GROQ_API_KEY=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
railway variables set YOUR_API_KEY=your-secret-api-key-123

# Deploy
railway up

# Generate a public domain
railway domain
```

---

## Testing Your Deployed API

### Step 1: Update Test Script

Edit `test_api.py` and change the BASE_URL:

```python
BASE_URL = "https://your-railway-url.up.railway.app"  # Your Railway URL
```

### Step 2: Run Tests

```bash
python test_api.py
```

### Step 3: Manual Testing with curl

```bash
# Replace YOUR_RAILWAY_URL with your actual Railway URL
curl -X POST https://YOUR_RAILWAY_URL/api/message \
  -H "x-api-key: your-secret-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "manual-test-001",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked! Verify now!",
      "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

Expected response:
```json
{
  "status": "success",
  "reply": "Why is my account being blocked?"
}
```

### Step 4: Check Health Endpoint

```bash
curl https://YOUR_RAILWAY_URL/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

---

## How to Submit to GUVI

Once deployed, provide GUVI with:

1. **Your Public API URL**: `https://your-app.up.railway.app/api/message`
2. **Your API Key**: `your-secret-api-key-123`

GUVI will send requests in this format:

```
POST https://your-app.up.railway.app/api/message
Headers:
  x-api-key: your-secret-api-key-123
  Content-Type: application/json

Body: {
  "sessionId": "...",
  "message": {...},
  "conversationHistory": [...],
  "metadata": {...}
}
```

Your API will:
1. Detect if it's a scam
2. Engage with the AI agent
3. Extract intelligence
4. After 8-12 messages, automatically send final results to:
   `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

---

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Railway deployment fails

**Solution**: Check Railway logs
```bash
railway logs
```

Common fixes:
- Ensure Dockerfile is correct
- Check environment variables are set
- Verify Python version compatibility

### Issue: Groq API errors

**Solution**: 
- Verify your Groq API key is correct
- Check Groq API status: https://status.groq.com
- Ensure you haven't hit rate limits

### Issue: API returns 401 Unauthorized

**Solution**: 
- Make sure `x-api-key` header is included
- Verify the API key matches your `YOUR_API_KEY` environment variable

### Issue: No response from agent

**Solution**:
- Check Railway logs for errors
- Verify Groq API key is valid
- Ensure the message triggers scam detection

### Issue: Final result not sent to GUVI

**Solution**:
- Check if conversation reached 8+ messages
- Verify intelligence was extracted
- Check Railway logs for callback errors

---

## Monitoring Your Deployment

### View Logs

**Railway Dashboard:**
1. Go to your project
2. Click on your service
3. Go to "Deployments" tab
4. Click on latest deployment
5. View logs in real-time

**Railway CLI:**
```bash
railway logs
```

### Check Metrics

Railway Dashboard → Your Service → Metrics

Monitor:
- CPU usage
- Memory usage
- Request count
- Response times

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    GUVI Platform                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ POST /api/message
                     │ (with x-api-key header)
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Railway (Your Deployment)                  │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         FastAPI Application                     │    │
│  │                                                  │    │
│  │  1. Receive Message                             │    │
│  │  2. Detect Scam (Keywords + Patterns)           │    │
│  │  3. Activate AI Agent if scam detected          │    │
│  │  4. Generate Response (Groq Llama 3.3)          │    │
│  │  5. Extract Intelligence                         │    │
│  │  6. Store in session                            │    │
│  │  7. After 8-12 msgs, send final result          │    │
│  │                                                  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────┬───────────────────────────────────┘
                       │
                       │ POST final result
                       │ (after conversation ends)
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│     https://hackathon.guvi.in/api/                      │
│              updateHoneyPotFinalResult                  │
│                                                          │
│  Receives:                                              │
│  - sessionId                                            │
│  - scamDetected: true                                   │
│  - totalMessagesExchanged                               │
│  - extractedIntelligence                                │
│  - agentNotes                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Key Features of Your Solution

✅ **Scam Detection**: Uses 20+ keywords and pattern matching
✅ **AI Agent**: Groq's Llama 3.3 70B model for human-like responses
✅ **Multi-turn**: Handles conversations across multiple messages
✅ **Intelligence Extraction**: Regex-based extraction of:
   - Bank accounts
   - UPI IDs
   - Phone numbers
   - Phishing links
   - Suspicious keywords
✅ **Automatic Reporting**: Sends results to GUVI after sufficient engagement
✅ **Session Management**: Tracks conversation state per session
✅ **Fast & Scalable**: Groq provides fast inference, Railway handles scaling

---

## Final Checklist Before Submission

- [ ] Code pushed to GitHub
- [ ] Deployed on Railway
- [ ] Public URL generated
- [ ] Environment variables set (GROQ_API_KEY, YOUR_API_KEY)
- [ ] Health endpoint tested (`/health`)
- [ ] Message endpoint tested (`/api/message`)
- [ ] Test conversation completed successfully
- [ ] Verified final result callback works
- [ ] API key documented for GUVI submission
- [ ] Public URL documented for GUVI submission

---

## Contact & Support

If you encounter issues:
1. Check Railway logs
2. Review this guide
3. Test locally first
4. Check Groq API status

Good luck with the competition! 🚀
