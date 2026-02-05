# Agentic Honey-Pot for Scam Detection

An AI-powered honeypot system that detects scam messages, engages scammers autonomously, and extracts intelligence.

##  Features

- **Scam Detection**: Automatically detects fraudulent messages using keyword analysis and pattern matching
- **AI Agent**: Uses Groq's Llama model to engage scammers in human-like conversations
- **Intelligence Extraction**: Automatically extracts bank accounts, UPI IDs, phone numbers, and phishing links
- **Multi-turn Conversations**: Maintains context across conversation sessions
- **Automated Reporting**: Sends final results to GUVI evaluation endpoint

##  Architecture

```
┌─────────────┐
│  Platform   │
│  (GUVI)     │
└──────┬──────┘
       │ POST /api/message
       ▼
┌─────────────────────────────┐
│   FastAPI Application       │
│                             │
│  ┌─────────────────────┐   │
│  │  Scam Detector      │   │
│  └─────────────────────┘   │
│           │                 │
│           ▼                 │
│  ┌─────────────────────┐   │
│  │  AI Agent (Groq)    │   │
│  │  - Llama 3.3 70B    │   │
│  └─────────────────────┘   │
│           │                 │
│           ▼                 │
│  ┌─────────────────────┐   │
│  │ Intelligence        │   │
│  │ Extractor           │   │
│  └─────────────────────┘   │
└──────────┬──────────────────┘
           │ POST final result
           ▼
┌─────────────────────────────┐
│  GUVI Evaluation Endpoint   │
└─────────────────────────────┘
```

##  Requirements

- Python 3.11+
- Groq API Key
- FastAPI
- Docker (for containerization)

##  Local Setup

1. **Clone/Create the project**
```bash
mkdir honeypot-api
cd honeypot-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your keys
nano .env
```

4. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

##  Docker Deployment

1. **Build the Docker image**
```bash
docker build -t honeypot-api .
```

2. **Run the container**
```bash
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_groq_key \
  -e YOUR_API_KEY=your_secret_key \
  honeypot-api
```

##  Railway Deployment

1. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize project**
```bash
railway init
```

4. **Set environment variables**
```bash
railway variables set GROQ_API_KEY=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
railway variables set YOUR_API_KEY=your-secret-api-key-123
```

5. **Deploy**
```bash
railway up
```

6. **Get your public URL**
```bash
railway domain
```

### Alternative: Deploy via Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Add environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `YOUR_API_KEY`: Your authentication key
5. Railway will auto-deploy from Dockerfile
6. Copy your public domain URL

## 📡 API Usage

### Endpoint: POST /api/message

**Headers:**
```
x-api-key: your-secret-api-key-123
Content-Type: application/json
```

**Request Body (First Message):**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Why is my account being blocked?"
}
```

**Request Body (Follow-up Message):**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Share your UPI ID to avoid suspension.",
    "timestamp": 1770005528732
  },
  "conversationHistory": [
    {
      "sender": "scammer",
      "text": "Your bank account will be blocked today. Verify immediately.",
      "timestamp": 1770005528731
    },
    {
      "sender": "user",
      "text": "Why is my account being blocked?",
      "timestamp": 1770005528731
    }
  ],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

##  Testing

Test your API with curl:

```bash
curl -X POST https://your-railway-url.up.railway.app/api/message \
  -H "x-api-key: your-secret-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-session-123",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked. Verify now!",
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

##  How It Works

1. **Scam Detection**: Analyzes incoming messages for scam patterns
2. **Agent Activation**: If scam detected, AI agent takes over
3. **Human-like Engagement**: Agent responds naturally to extract information
4. **Intelligence Extraction**: Automatically extracts:
   - Bank account numbers
   - UPI IDs
   - Phishing links
   - Phone numbers
   - Suspicious keywords
5. **Final Report**: After 8-12 messages, sends final intelligence to GUVI endpoint

##  Security

- API key authentication required
- No storage of sensitive user data
- Ethical engagement only
- No impersonation of real individuals

##  Evaluation Criteria

- Scam detection accuracy
- Quality of AI engagement
- Intelligence extraction effectiveness
- API stability and response time
- Ethical behavior

## Tech Stack

- **FastAPI**: Web framework
- **Groq**: AI model inference (Llama 3.3 70B)
- **Python 3.11**: Programming language
- **Docker**: Containerization
- **Railway**: Deployment platform

## Project Structure

```
honeypot-api/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .env.example        # Environment variables template
├── README.md           # Documentation
└── test_api.py         # Test script
```



For issues or questions about the competition, contact GUVI support.

## 📄 License

This project is for hackathon use only.
