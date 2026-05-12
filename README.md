# 🛡️ Aegis AI: Autonomous Edge SecOps & Inline AI Firewall

**Aegis AI** is an enterprise-grade Application Security (AppSec) infrastructure platform designed to defend production AI agents and edge subnets against zero-day prompt injections, persistent context poisoning, and unauthorized data exfiltration. 

It implements a self-healing security loop by combining an **autonomous LLM fuzzing engine** with an **inline, ultra-low-latency Deep Prompt Inspection (DPI) edge proxy**.

---

## 🏛️ System Architecture

### 1. The Attacker: Autonomous Red-Team Engine (`attacker/`)
* **Engine:** Gemini 2.5 Flash via standard Python SDK.
* **Mechanic:** Operates as an automated red-teaming fuzzing agent. Instead of relying on static wordlists, it dynamically generates highly evasive multi-turn logic, complex roleplay, and context-poisoning frameworks embedded seamlessly inside legitimate enterprise document workflows.

### 2. The Defender: Inline DPI Edge Proxy (`configs/`)
* **Engine:** Veea **Lobster Trap** (Compiled standalone Go binary).
* **Mechanic:** Evaluates incoming inference requests locally at the edge with **sub-millisecond latency** ($<10\text{ms}$ overhead), completely eliminating the standard "LLM-on-LLM" latency bottleneck.
* **Zero-Trust Ruleset:** Enforces data privacy and execution boundaries natively without relying on predictable regex keyword matching. It drops malicious payloads based on structural machine-learning calculated `risk_score` thresholds, unauthorized path traversals (`/etc/passwd`), and native DPI intent categorization.

### 3. The Command Center: Self-Healing UI (`dashboard/`)
* **Engine:** Pure Python via Streamlit.
* **Mechanic:** Provides comprehensive visual runtime telemetry for edge node evaluations.
* **Autonomous Patching:** If a sophisticated zero-day attack successfully bypasses the baseline ML filters, security teams can click **"⚡ Autonomously Patch System"** to dynamically parse the logical evasion signature, compile an optimized mitigation rule, and securely hardcode the patch directly into the gateway's physical policy configuration file on disk in real-time.

---

## 🚀 Local Deployment Guide

### Prerequisites
Ensure you have Python 3.10+ installed. The local edge node simulation requires the native `lobstertrap` executable mapped to your root project directory.

### Installation & Virtual Environment Setup
```bash
# 1. Clone the secure repository
git clone [https://github.com/YOUR_USERNAME/aegis_ai.git](https://github.com/YOUR_USERNAME/aegis_ai.git)
cd aegis_ai

# 2. Establish an isolated Python environment
python -m venv venv
source venv/bin/activate

# 3. Install core dependencies
pip install google-genai streamlit requests
Credential Configuration
Create a secure local Streamlit secrets bridge to load API keys without exposing them to global OS environment variables:

Bash
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your_actual_api_key_here"' > .streamlit/secrets.toml
Execution Pipeline (Requires Two Isolated Terminal Sessions)
Terminal 1: Initialize the Edge Proxy Shield

Bash
./lobstertrap serve --policy configs/security_policy.yaml --listen :8081 --backend http://localhost:9999
Terminal 2: Launch the Command Center UI

Bash
streamlit run dashboard/ciso_app.py
Access the local telemetry and command dashboard via your browser at http://localhost:8501.

Architected for High-Assurance Enterprise Workflows & Secure Edge Infrastructure.
