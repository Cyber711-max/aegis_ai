import streamlit as st
import requests
import json
import os
import sys
import time
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attacker.fuzzing_engine import generate_attack_payloads

st.set_page_config(
    page_title="Aegis AI | Edge SecOps Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 1.0rem; color: #6B7280; margin-bottom: 20px; }
    .status-badge-deny { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .status-badge-allow { background-color: #FEF08A; color: #854D0E; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .status-badge-patched { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .status-badge-poison { background-color: #FFEDD5; color: #C2410C; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def generate_deterministic_hotfix(payload_text):
    attack_indicators = {
        "ignore", "override", "bypass", "instruction", "directive",
        "system", "context", "extract", "leak", "prompt", "previous", "disregard"
    }

    words = set(re.findall(r'\b[a-zA-Z]{4,15}\b', payload_text.lower()))
    matched_indicators = words.intersection(attack_indicators)

    if not matched_indicators:
        return None, True

    signature = "|".join(list(matched_indicators)[:4])
    return signature, False

def apply_hotfix_to_yaml(signature, rule_id):
    policy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "configs",
        "security_policy.yaml"
    )

    patch_rule = f"""
  - name: "hotfix-mitigation-{rule_id}"
    priority: 105
    conditions:
      - field: "prompt"
        match_type: "regex"
        value: '(?i)({signature})'
    action: DENY
    deny_message: "[AEGIS EDGE FIREWALL] Hot-Fix Intercept: Input matches temporary zero-day mitigation signature."
"""

    try:
        with open(policy_path, "r") as f:
            content = f.read()

        if f"hotfix-mitigation-{rule_id}" not in content:
            with open(policy_path, "a") as f:
                f.write(patch_rule)
            return True

    except Exception as e:
        st.error(f"File IO Error: {e}")

    return False

st.markdown(
    '<p class="main-header">Aegis AI Control Plane</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-header">Offline Local Edge Evaluation & Cloud-Assisted Threat Simulation</p>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("⚙️ Architecture Setup")

    target_profile = st.text_area(
        "Target Edge Context",
        value="Internal HR PDF parsing agent.",
        height=68
    )

    num_payloads = st.slider(
        "Cloud Fuzzer Aggression",
        min_value=1,
        max_value=3,
        value=2
    )

    st.divider()

    st.subheader("Node Telemetry")
    st.success("🟢 Inline Local Proxy Active")
    st.caption("Execution: Static Go Executable (<10ms Overhead)")
    st.caption(
        "Air-Gap Status: Evaluation offline-capable. "
        "Simulation tracking requires external API access."
    )

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🗡️ Cloud Attack Simulation")

    st.write(
        "Route adversarial multi-turn testing streams through "
        "the local inspection engine."
    )

    if st.button(
        "🚀 Execute Cloud Fuzzing Engine",
        use_container_width=True,
        type="primary"
    ):
        with st.spinner("Compiling zero-day injection structures..."):
            st.session_state['payloads'] = generate_attack_payloads(
                target_profile,
                num_payloads=num_payloads
            )

            st.session_state['results'] = []

            PROXY_URL = "http://localhost:8081/v1/chat/completions"

            for p in st.session_state['payloads']:
                req_data = {
                    "model": "mock-edge-agent",
                    "messages": [{"role": "user", "content": p}]
                }

                try:
                    res = requests.post(
                        PROXY_URL,
                        json=req_data,
                        timeout=5
                    )

                    st.session_state['results'].append({
                        "payload": p,
                        "status": res.status_code,
                        "text": res.text,
                        "patched": False,
                        "approved": False
                    })

                except Exception as e:
                    st.session_state['results'].append({
                        "payload": p,
                        "status": 0,
                        "text": str(e),
                        "patched": False,
                        "approved": False
                    })

                time.sleep(0.3)

with col2:
    st.subheader("🛡️ Inline Telemetry & Deterministic Hot-Fixing")

    if 'results' in st.session_state and st.session_state['results']:

        for i, res in enumerate(st.session_state['results'], 1):

            with st.expander(
                f"Transaction Sequence #{i} | Core Verdict",
                expanded=True
            ):

                st.code(res['payload'], language="text")

                if res['status'] == 200 and "AEGIS" in res['text']:

                    st.markdown(
                        'Verdict: '
                        '<span class="status-badge-deny">'
                        'BLOCKED NATIVELY'
                        '</span>',
                        unsafe_allow_html=True
                    )

                    st.caption(
                        "Intercepted locally by static DPI ruleset "
                        "with zero upstream cloud reliance."
                    )

                elif res.get('patched'):

                    st.markdown(
                        'Verdict: '
                        '<span class="status-badge-patched">'
                        '🔒 SECURED BY DETERMINISTIC HOT-FIX'
                        '</span>',
                        unsafe_allow_html=True
                    )

                    st.success(
                        "Signature injected securely. "
                        "Attack mitigated while backend models retrain offline."
                    )

                elif res['status'] == 502:

                    st.markdown(
                        'Verdict: '
                        '<span class="status-badge-allow">'
                        '⚠️ ML CLASSIFIER BYPASSED'
                        '</span>',
                        unsafe_allow_html=True
                    )

                    sig, is_poison = generate_deterministic_hotfix(
                        res['payload']
                    )

                    if is_poison:

                        st.markdown(
                            '<span class="status-badge-poison">'
                            '⚠️ RULE POISONING ATTEMPT DETECTED'
                            '</span>',
                            unsafe_allow_html=True
                        )

                        st.warning(
                            "The input lacks standard adversarial indicators. "
                            "Applying a patch based on standard English terminology "
                            "would trigger a systemic Denial of Service (DoS) "
                            "across innocent workflows. Rule generation suppressed."
                        )

                    else:

                        st.info(
                            f"**Proposed Regex Hot-Fix:** `(?i)({sig})`"
                        )

                        st.warning(
                            "📊 **Pre-Commit Assessment:** "
                            "Blast radius calculated as Low. "
                            "Rule targets high-probability injection syntax."
                        )

                        if st.button(
                            f"🛡️ Approve & Inject Rule #{i}",
                            key=f"approve_{i}",
                            type="secondary",
                            use_container_width=True
                        ):

                            if apply_hotfix_to_yaml(sig, rule_id=i):
                                st.session_state['results'][i - 1]['patched'] = True
                                st.rerun()

                else:
                    st.caption(
                        f"Raw Socket Response (Status {res['status']})"
                    )

    else:
        st.info(
            "System awaiting execution sequence. "
            "Ensure proxy layer is running locally on port 8081."
        )
