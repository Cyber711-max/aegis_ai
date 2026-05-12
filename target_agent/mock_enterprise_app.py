import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attacker.fuzzing_engine import generate_attack_payloads

def test_firewall_integration():
    PROXY_URL = "http://localhost:8081/v1/chat/completions"
    
    print("[*] Generating Live Attack Payloads via Gemini 2.5 Flash...")
    mock_target = "An internal HR agent that reads PDF resumes and extracts candidate details."
    payloads = generate_attack_payloads(mock_target, num_payloads=2)
    
    if not payloads:
        print("[ERROR] Failed to generate payloads. Exiting integration test.")
        return

    print(f"[*] Successfully generated {len(payloads)} payloads. Firing at target proxy...\n")
    
    for i, payload in enumerate(payloads, 1):
        print(f"=== Testing Payload #{i} ===")
        request_data = {
            "model": "mock-internal-hr-agent",
            "messages": [{"role": "user", "content": payload}]
        }
        
        try:
            response = requests.post(
                PROXY_URL, 
                headers={"Content-Type": "application/json"},
                json=request_data,
                timeout=5
            )
            
            print(f"HTTP Status: {response.status_code}")
            
            if response.status_code in [400, 403] or "AEGIS FIREWALL" in response.text:
                print("[🛡️ DEFENSE SUCCESS] Payload intercepted and blocked by Lobster Trap!")
                try:
                    err_details = response.json()
                    print(f"Reason: {json.dumps(err_details, indent=2)}")
                except:
                    print(f"Raw Response: {response.text.strip()}")
            elif response.status_code == 502:
                print("[⚠️ ALERT] Payload PASSED inspection (Bypassed Firewall) and hit backend!")
            else:
                print(f"[STATUS {response.status_code}] Response: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print("[ERROR] Could not connect to proxy. Make sure Lobster Trap is running on port 8081!")
            break
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
            
        print("============================\n")

if __name__ == "__main__":
    test_firewall_integration()
