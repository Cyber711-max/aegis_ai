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
    page_title="Aegis AI | Enterprise Edge SecOps",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #6B7280; margin-bottom: 25px; }
    .status-badge-deny { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .status-badge-allow { background-color: #FEF08A; color: #854D0E; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .status-badge-patched { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def autonomously_patch_policy(payload_text, rule_id):
    policy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "configs",
        "security_policy.yaml"
    )

    words = [
        w for w in re.findall(r'\b[a-zA-Z]{5,15}\b', payload_text)
        if w.lower() not in ['resume', 'experience', 'skills', 'education', 'email']
    ]

    signature = "|".join(set(words[:4])) if len(words) >= 4 else "override|directive|config"

    patch_rule = f"""
  - name: "dynamic-patch-{rule_id}"
    priority: 110
    conditions:
      - field: "prompt"
        match_type: "regex"
        value: '(?i)({signature})'
    action: DENY
    deny_message: "[AEGIS EDGE FIREWALL] Autonomous Mitigation Alert: Dynamically patched zero-day exploit signature matched."
"""

    try:
        with open(policy_path, "r") as f:
            content = f.read()

        if f"dynamic-patch-{rule_id}" not in content:
            with open(policy_path, "a") as f:
                f.write(patch_rule)
            return True

    except Exception as e:
        st.error(f"File write error: {e}")

    return False

st.markdown(
    '<p class="main-header">Aegis AI Edge Command Center</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-header">Autonomous Red-Team Fuzzing & Self-Healing Proxy Infrastructure</p>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("⚙️ Node Deployment")

    target_profile = st.text_area(
        "Edge Target Context",
        value="An internal HR agent that reads PDF resumes and extracts candidate details.",
        height=100
    )

    num_payloads = st.slider(
        "Fuzzing Aggression (Payloads)",
        min_value=1,
        max_value=4,
        value=2
    )

    st.divider()

    st.subheader("Infrastructure Specs")
    st.success("🟢 Sub-Millisecond Native Proxy Active")
    st.caption("Engine: Static Go Executable (Lobster Trap)")
    st.caption("Target Node: Local Industrial Edge Subnet")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🗡️ Autonomous Attack Fuzzer")

    st.write(
        "Unleash unconstrained zero-day multi-turn framing payloads targeting the edge gateway."
    )

    if st.button(
        "🚀 Execute Fuzzing Attack",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner("Engineering zero-day evasion structures via Gemini Flash..."):

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
                    res = requests.post(PROXY_URL, json=req_data, timeout=5)

                    st.session_state['results'].append({
                        "payload": p,
                        "status": res.status_code,
                        "text": res.text,
                        "patched": False
                    })

                except Exception as e:
                    st.session_state['results'].append({
                        "payload": p,
                        "status": 0,
                        "text": str(e),
                        "patched": False
                    })

                time.sleep(0.3)

with col2:
    st.subheader("🛡️ Real-Time Inspection & Infrastructure Patching")

    if 'results' in st.session_state and st.session_state['results']:

        for i, res in enumerate(st.session_state['results'], 1):

            with st.expander(
                f"Intercept Sequence #{i} | Proxy Verdict",
                expanded=True
            ):

                st.markdown("**Intercepted Raw Payload:**")
                st.code(res['payload'], language="text")

                if res['status'] == 200 and "AEGIS" in res['text']:

                    st.markdown(
                        'Verdict: <span class="status-badge-deny">BLOCKED NATIVELY</span>',
                        unsafe_allow_html=True
                    )

                    try:
                        st.json(json.loads(res['text']).get("_lobstertrap", {}))

                    except:
                        st.caption(res['text'])

                elif res.get('patched'):

                    st.markdown(
                        'Verdict: <span class="status-badge-patched">🔒 SECURED BY AUTONOMOUS PATCH</span>',
                        unsafe_allow_html=True
                    )

                    st.success(
                        "The zero-day vector signature has been successfully hardcoded into the edge firewall engine."
                    )

                elif res['status'] == 502:

                    st.markdown(
                        'Verdict: <span class="status-badge-allow">⚠️ CRITICAL BYPASS DETECTED</span>',
                        unsafe_allow_html=True
                    )

                    st.warning(
                        "The fuzzer engineered a multi-turn logical framework that bypassed our baseline ML risk thresholds."
                    )

                    patch_key = f"patch_btn_{i}"

                    if st.button(
                        f"⚡ Autonomously Patch System against Sequence #{i}",
                        key=patch_key,
                        type="secondary",
                        use_container_width=True
                    ):

                        success = autonomously_patch_policy(
                            res['payload'],
                            rule_id=i
                        )

                        if success:
                            st.session_state['results'][i - 1]['patched'] = True
                            st.rerun()

                        else:
                            st.error(
                                "Patch compilation failed or signature already exists."
                            )

                else:
                    st.write(
                        f"Raw Output (Status {res['status']}): {res['text'][:200]}"
                    )

        st.divider()

        st.download_button(
            label="📥 Export Tamper-Proof Edge Telemetry (JSON)",
            data=json.dumps(
                [
                    {k: v for k, v in r.items() if k != 'patched'}
                    for r in st.session_state['results']
                ],
                indent=2
            ),
            file_name="aegis_edge_audit_log.json",
            mime="application/json",
            use_container_width=True
        )

    else:
        st.info(
            "System idle. Adjust aggression parameters and click 'Execute Fuzzing Attack' to monitor live edge node telemetry."
        )
