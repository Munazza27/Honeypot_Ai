from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime
import os
from groq import Groq
import requests
import re
import json

app = FastAPI(title="Agentic Honey-Pot API")

# Your Groq API Key

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

YOUR_API_KEY = os.environ.get("YOUR_API_KEY", "your-secret-api-key-123")


# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Store session data in memory (use Redis/Database in production)
session_store: Dict[str, Dict] = {}

# Pydantic Models
class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class Metadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

class AgentResponse(BaseModel):
    status: str
    reply: str

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

class FinalResultPayload(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str


# Scam Detection Module
class ScamDetector:
    SCAM_KEYWORDS = [
        "account blocked", "verify immediately", "urgent", "suspended", 
        "click here", "confirm your", "update your details", "prize won",
        "lottery", "refund", "kbc", "tax refund", "verify now", "otp",
        "bank account", "credit card", "debit card", "cvv", "pin",
        "transaction failed", "unusual activity", "secure your account",
        "limited time", "act now", "congratulations", "you won"
    ]
    
    @staticmethod
    def detect_scam(text: str) -> bool:
        """Detect if a message is likely a scam"""
        text_lower = text.lower()
        
        # Check for scam keywords
        keyword_matches = sum(1 for keyword in ScamDetector.SCAM_KEYWORDS if keyword in text_lower)
        
        # Check for urgency patterns
        urgency_patterns = [
            r"(urgent|immediate|now|today|asap)",
            r"(block|suspend|deactivate|freeze)",
            r"(verify|confirm|update|secure)"
        ]
        urgency_score = sum(1 for pattern in urgency_patterns if re.search(pattern, text_lower))
        
        # Scam detection logic
        if keyword_matches >= 2 or urgency_score >= 2:
            return True
        
        return False


# Intelligence Extractor
class IntelligenceExtractor:
    @staticmethod
    def extract(conversation_history: List[Message]) -> ExtractedIntelligence:
        """Extract intelligence from conversation"""
        intelligence = ExtractedIntelligence()
        
        all_text = " ".join([msg.text for msg in conversation_history])
        
        # Extract bank accounts (simple pattern)
        bank_accounts = re.findall(r'\b\d{9,18}\b', all_text)
        intelligence.bankAccounts = list(set(bank_accounts))
        
        # Extract UPI IDs
        upi_ids = re.findall(r'\b[\w\.\-]+@[\w]+\b', all_text)
        intelligence.upiIds = list(set(upi_ids))
        
        # Extract URLs/Links
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', all_text)
        intelligence.phishingLinks = list(set(urls))
        
        # Extract phone numbers
        phones = re.findall(r'\+?[\d\s\-\(\)]{10,}', all_text)
        intelligence.phoneNumbers = list(set([p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]))
        
        # Extract suspicious keywords
        for keyword in ScamDetector.SCAM_KEYWORDS:
            if keyword.lower() in all_text.lower():
                intelligence.suspiciousKeywords.append(keyword)
        
        intelligence.suspiciousKeywords = list(set(intelligence.suspiciousKeywords))
        
        return intelligence


# AI Agent
class HoneyPotAgent:
    def __init__(self):
        self.client = groq_client
        self.model = "llama-3.3-70b-versatile"  # Fast and capable model
    
    def generate_response(self, message: str, conversation_history: List[Message], session_data: Dict) -> str:
        """Generate human-like response to engage scammer"""
        
        # Build conversation context
        context = self._build_context(conversation_history, session_data)
        
        # Create the prompt for the AI
        system_prompt = """You are roleplaying as a regular person who has received a suspicious message. 
Your goal is to:
1. Act curious and concerned (like a real potential victim would)
2. Ask questions that help extract information (bank accounts, UPI IDs, phone numbers, links)
3. Never reveal you know it's a scam
4. Be naturally hesitant about sharing personal info, but curious enough to keep the conversation going
5. Use simple, casual language with occasional typos or informal speech
6. Show some trust but ask for clarification on suspicious requests
7. Keep responses SHORT (1-2 sentences max)

Be believable. Sound like a real person who is concerned but not tech-savvy."""

        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            role = "assistant" if msg.sender == "user" else "user"
            messages.append({"role": role, "content": msg.text})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Generate response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=150,
            )
            
            reply = response.choices[0].message.content.strip()
            return reply
            
        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback responses
            fallback_responses = [
                "Why is this happening?",
                "What do you need from me?",
                "Is this really from my bank?",
                "Can you give me more details?"
            ]
            return fallback_responses[len(conversation_history) % len(fallback_responses)]
    
    def _build_context(self, conversation_history: List[Message], session_data: Dict) -> str:
        """Build context from conversation"""
        context = f"Messages exchanged: {session_data.get('message_count', 0)}\n"
        context += f"Scam detected: {session_data.get('scam_detected', False)}\n"
        return context


# Background task to send final result
def send_final_result(session_id: str, session_data: Dict):
    """Send final result to GUVI endpoint"""
    
    # Extract intelligence
    all_messages = session_data.get('all_messages', [])
    intelligence = IntelligenceExtractor.extract(all_messages)
    
    # Prepare payload
    payload = {
        "sessionId": session_id,
        "scamDetected": session_data.get('scam_detected', False),
        "totalMessagesExchanged": session_data.get('message_count', 0),
        "extractedIntelligence": {
            "bankAccounts": intelligence.bankAccounts,
            "upiIds": intelligence.upiIds,
            "phishingLinks": intelligence.phishingLinks,
            "phoneNumbers": intelligence.phoneNumbers,
            "suspiciousKeywords": intelligence.suspiciousKeywords
        },
        "agentNotes": session_data.get('agent_notes', 'Scam engagement completed')
    }
    
    try:
        response = requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        print(f"Final result sent for session {session_id}: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending final result: {e}")


# API Endpoints
@app.post("/api/message", response_model=AgentResponse)
async def handle_message(
    request: IncomingRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
):
    """Main endpoint to receive and process messages"""
    
    # Validate API key
    if x_api_key != YOUR_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    session_id = request.sessionId
    incoming_message = request.message
    conversation_history = request.conversationHistory
    
    # Initialize or update session data
    if session_id not in session_store:
        session_store[session_id] = {
            'scam_detected': False,
            'message_count': 0,
            'all_messages': [],
            'agent_notes': '',
            'agent_active': False
        }
    
    session_data = session_store[session_id]
    session_data['message_count'] += 1
    session_data['all_messages'].append(incoming_message)
    
    # Detect scam on first message or if not yet detected
    if not session_data['scam_detected']:
        is_scam = ScamDetector.detect_scam(incoming_message.text)
        if is_scam:
            session_data['scam_detected'] = True
            session_data['agent_active'] = True
            session_data['agent_notes'] = 'Scam detected. Agent activated for intelligence extraction.'
    
    # If scam detected, activate AI agent
    if session_data['agent_active']:
        agent = HoneyPotAgent()
        
        # Reconstruct full conversation history
        full_history = conversation_history + [incoming_message]
        
        # Generate response
        reply = agent.generate_response(
            incoming_message.text,
            conversation_history,
            session_data
        )
        
        # Store agent's response
        agent_message = Message(
            sender="user",
            text=reply,
            timestamp=int(datetime.now().timestamp() * 1000)
        )
        session_data['all_messages'].append(agent_message)
        
        # Check if we should end conversation and send final result
        # End after 8-12 messages or if we've extracted good intelligence
        if session_data['message_count'] >= 8:
            intelligence = IntelligenceExtractor.extract(session_data['all_messages'])
            
            # Check if we have valuable intelligence
            has_intelligence = (
                len(intelligence.bankAccounts) > 0 or
                len(intelligence.upiIds) > 0 or
                len(intelligence.phishingLinks) > 0 or
                len(intelligence.phoneNumbers) > 0
            )
            
            if has_intelligence or session_data['message_count'] >= 12:
                # Send final result in background
                background_tasks.add_task(send_final_result, session_id, session_data)
        
        return AgentResponse(status="success", reply=reply)
    
    else:
        # No scam detected - send generic response
        return AgentResponse(
            status="success",
            reply="I'm sorry, I didn't understand. Can you clarify?"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Agentic Honey-Pot API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
