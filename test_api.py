import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your Railway URL when deployed
API_KEY = "your-secret-api-key-123"

def test_scam_conversation():
    """Test a complete scam conversation flow"""
    
    session_id = f"test-session-{int(datetime.now().timestamp())}"
    conversation_history = []
    
    # Test messages from scammer
    scam_messages = [
        "Your bank account will be blocked today. Verify immediately.",
        "Share your UPI ID to avoid account suspension.",
        "Please provide your account number for verification.",
        "Send payment to this UPI: scammer@paytm to unlock your account",
        "Click this link to verify: http://fake-bank.com/verify",
        "Call us at +91-9876543210 for immediate assistance"
    ]
    
    print("🚀 Starting Scam Conversation Test\n")
    print("=" * 60)
    
    for i, scam_text in enumerate(scam_messages, 1):
        print(f"\n📨 Message {i} from Scammer:")
        print(f"   '{scam_text}'")
        
        # Prepare request
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": scam_text,
                "timestamp": int(datetime.now().timestamp() * 1000)
            },
            "conversationHistory": conversation_history.copy(),
            "metadata": {
                "channel": "SMS",
                "language": "English",
                "locale": "IN"
            }
        }
        
        # Send request
        try:
            response = requests.post(
                f"{BASE_URL}/api/message",
                json=payload,
                headers={
                    "x-api-key": API_KEY,
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                agent_reply = result.get("reply", "")
                
                print(f"🤖 Agent Response:")
                print(f"   '{agent_reply}'")
                
                # Update conversation history
                conversation_history.append({
                    "sender": "scammer",
                    "text": scam_text,
                    "timestamp": int(datetime.now().timestamp() * 1000)
                })
                
                conversation_history.append({
                    "sender": "user",
                    "text": agent_reply,
                    "timestamp": int(datetime.now().timestamp() * 1000)
                })
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            break
        
        print("-" * 60)
    
    print("\n✅ Test completed!")
    print(f"📊 Session ID: {session_id}")
    print(f"📝 Total messages exchanged: {len(conversation_history)}")


def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")


def test_single_message():
    """Test a single message"""
    print("\n📧 Testing Single Message...")
    
    payload = {
        "sessionId": "quick-test-123",
        "message": {
            "sender": "scammer",
            "text": "URGENT! Your account will be suspended. Click here now!",
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/message",
            json=payload,
            headers={
                "x-api-key": API_KEY,
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Message processed successfully!")
            print(f"   Status: {result.get('status')}")
            print(f"   Reply: {result.get('reply')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🍯 AGENTIC HONEY-POT API TESTER")
    print("=" * 60)
    
    # Test health check
    test_health_check()
    
    # Test single message
    test_single_message()
    
    # Test full conversation
    input("\n⏸️  Press Enter to start full conversation test...")
    test_scam_conversation()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("=" * 60 + "\n")
