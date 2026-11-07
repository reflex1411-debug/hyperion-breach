import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="HYPERION CLOUD // SECURE TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Determine CSS theme based on Act 2 status (Act 1 = Amber Startup / Act 2 = CRT Green NORAD)
act_2_is_active = st.session_state.get("act_2_active", False)

primary_color = "#00ff66" if act_2_is_active else "#ffb000"
bg_color = "#020804" if act_2_is_active else "#050505"
panel_bg = "#08140c" if act_2_is_active else "#111111"
border_color = "#00ff66" if act_2_is_active else "#332600"

st.markdown(f"""
    <style>
    /* Hide default Streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Global Terminal Theme */
    .stApp {{
        background-color: {bg_color};
        color: {primary_color};
        font-family: 'Courier New', Courier, monospace;
    }}
    
    /* Startup / Retro Cards */
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {{
        background-color: {panel_bg};
        border: 2px solid {border_color};
        border-left: 6px solid {primary_color};
        padding: 20px;
        border-radius: 0px;
        margin-bottom: 15px;
    }}
    
    /* Headers */
    h1, h2, h3 {{
        font-family: 'Courier New', Courier, monospace;
        color: {primary_color} !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {panel_bg};
        color: {primary_color};
        border: 2px solid {primary_color};
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
    }}
    .stButton > button:hover {{
        background-color: {primary_color};
        color: {bg_color};
    }}
    
    /* Terminal Logs */
    .terminal-log {{
        background-color: #020402;
        border: 1px dashed {border_color};
        padding: 12px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.85rem;
        color: {primary_color};
        height: 150px;
        overflow-y: auto;
    }}
    
    /* DEFCON 1 Pulse Warning */
    .defcon-alert {{
        color: #ff0033 !important;
        border-color: #ff0033 !important;
        animation: pulse 1s infinite;
    }}
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.4; }}
        100% {{ opacity: 1; }}
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALIZE SESSION STATE
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "is_saboteur" not in st.session_state: st.session_state.is_saboteur = False
if "team_score" not in st.session_state: st.session_state.team_score = 1250
if "system_integrity" not in st.session_state: st.session_state.system_integrity = 88.4
if "act_2_active" not in st.session_state: st.session_state.act_2_active = False
if "defcon_level" not in st.session_state: st.session_state.defcon_level = 5
if "wopr_logs" not in st.session_state:
    st.session_state.wopr_logs = [
        "> INITIALIZING NORAD DEFENSE LINK...",
        "> CONNECTION TO WOPR SUPERCOMPUTER ESTABLISHED.",
        "> GREETINGS. SHALL WE PLAY A GAME?"
    ]
if "logs" not in st.session_state:
    st.session_state.logs = [
        "[09:00:12] - GITHUB HOOK: Main repository branch merged by @dev_lead.",
        "[10:14:20] - KUBERNETES POD: Cluster US-East autoscaled successfully.",
        "[11:05:00] - ANOMALY: Latency spike detected on Redis cache node 3."
    ]

# ==========================================
# 3. AUTHENTICATION GATE
# ==========================================
if not st.session_state.logged_in:
    st.markdown("# [SYS_ID: HYPERION_CLOUD // SECURE GATEWAY]")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### ENGINEER IDENTIFICATION REQUIRED")
        input_name = st.text_input("ENTER ENGINEER CODENAME:")
        input_pin = st.text_input("ENTER ACCESS TOKEN:", type="password")
        secret_saboteur_toggle = st.checkbox("[DEBUG] FLAG AS ACTIVE HACKER / MOLE")

        if st.button("ESTABLISH SSH TUNNEL"):
            if input_name.strip() != "":
                st.session_state.username = input_name
                st.session_state.logged_in = True
                st.session_state.is_saboteur = secret_saboteur_toggle
                st.rerun()
            else:
                st.error("ACCESS DENIED: Enter a valid engineer codename.")
    with col2:
        st.info("Welcome, Engineer. Protect the microservice architecture, debug routing errors, and secure our Series B infrastructure.")
    st.stop()

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown(f"### [USER: {st.session_state.username.upper()}]")
if st.session_state.is_saboteur:
    st.sidebar.error("CLEARANCE: LEVEL 5 // [ROGUE HACKER]")
else:
    st.sidebar.success("CLEARANCE: LEVEL 2 // [SYSTEM ENGINEER]")

st.sidebar.markdown("---")

nav_options = ["MISSION CONTROL", "CLOUD ROUTING MATRIX (PUZZLE)", "DAILY SECURITY AUDIT", "INTEL LEADERBOARD"]
if st.session_state.act_2_active:
    nav_options.append("🚨 ACT 2: WOPR // NORAD CONSOLE")

nav_choice = st.sidebar.radio("NAVIGATION CONSOLE", nav_options)

st.sidebar.markdown("---")
# Host toggle for Act 2 escalation
host_act2_toggle = st.sidebar.toggle("ACTIVATE ACT 2 (WARGAMES ESCALATION)", value=st.session_state.act_2_active)
if host_act2_toggle != st.session_state.act_2_active:
    st.session_state.act_2_active = host_act2_toggle
    if host_act2_toggle:
        st.session_state.logs.append(f"[{pd.Timestamp.now().strftime('%H:%M:%S')}] - [!] CRITICAL: External backdoor routed to NORAD WOPR mainframe.")
    st.rerun()

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# 5. VIEW 1: MISSION CONTROL
# ==========================================
if nav_choice == "MISSION CONTROL":
    if st.session_state.act_2_active:
        st.markdown("# [NORAD DEFENSE // ACT 2 ACTIVE]")
        st.warning("⚠️ WARNING: Terminal linked to military supercomputer simulation. DEFCON escalation in progress.")
    elif st.session_state.is_saboteur:
        st.markdown("# [ROOT ACCESS // HACKER CONSOLE]")
        st.error("WARNING: Root privileges active. You are embedded as the System Saboteur.")
    else:
        st.markdown("# [SYS_ID: HYPERION_CLOUD // MISSION CONTROL]")
    
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="SERVER UPTIME FUND", value=f"{st.session_state.team_score} PTS")
    with col2:
        st.metric(label="CLUSTER INTEGRITY", value=f"{st.session_state.system_integrity}%")
    with col3:
        status_label = "DEFCON 1 // CRITICAL" if st.session_state.defcon_level == 1 else "NOMINAL"
        st.metric(label="THREAT STATUS", value=f"DEFCON {st.session_state.defcon_level}" if st.session_state.act_2_active else status_label)

    st.markdown("### LIVE SERVER TELEMETRY LOG FEED")
    log_html = "<br>".join(st.session_state.logs)
    st.markdown(f'<div class="terminal-log">{log_html}</div>', unsafe_allow_html=True)

    # Saboteur / Hacker Payload Panel
    if st.session_state.is_saboteur:
        st.markdown("---")
        st.markdown("### 🔴 HACKER PAYLOAD DECK")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("[EXECUTE: INJECT API CORRUPTION]"):
                st.session_state.system_integrity = max(10.0, st.session_state.system_integrity - 7.5)
                st.session_state.logs.append(f"[{pd.Timestamp.now().strftime('%H:%M:%S')}] - [!] ANOMALY: Malicious commit injected by rogue process.")
                st.rerun()
        with col_h2:
            if st.button("[ESCALATE DEFCON LEVEL]"):
                if st.session_state.defcon_level > 1:
                    st.session_state.defcon_level -= 1
                    st.session_state.logs.append(f"[{pd.Timestamp.now().strftime('%H:%M:%S')}] - [!] ALERT: DEFCON escalated to {st.session_state.defcon_level}.")
                    st.rerun()

# ==========================================
# 6. VIEW 2: CLOUD ROUTING MATRIX (PUZZLE)
# ==========================================
elif nav_choice == "CLOUD ROUTING MATRIX (PUZZLE)":
    st.markdown("# [ACTIVE MISSION // CLOUD SERVER ROUTING MATRIX]")
    st.markdown("---")
    st.markdown("""
    **Directive:** A rogue push to the main repository has scrambled our microservice routing tables. Read the deployment clues below and match each region to its correct database shard to restore server stability.
    
    *Deployment Clues:*
    1. The Auth Service Shard is NOT hosted on the AWS US-East node.
    2. The GCP Europe node houses the Billing API.
    3. The Azure Asia-South node runs the Redis Cache.
    """)
    
    with st.form("puzzle_form"):
        node_us = st.selectbox("AWS US-East Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"])
        node_eu = st.selectbox("GCP Europe Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"])
        node_asia = st.selectbox("Azure Asia-South Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"])
        
        submit_puzzle = st.form_submit_button("[VERIFY ROUTING INTEGRITY]")
        if submit_puzzle:
            if node_eu == "Billing API" and node_asia == "Redis Cache" and node_us != "Auth Service Shard":
                st.session_state.system_integrity = min(100.0, st.session_state.system_integrity + 15.0)
                st.session_state.team_score += 250
                st.session_state.logs.append(f"[{pd.Timestamp.now().strftime('%H:%M:%S')}] - [OK] Server routing fixed by {st.session_state.username}.")
                st.success("ACCESS GRANTED: Microservice architecture restored! +250 Points.")
            else:
                st.session_state.logs.append(f"[{pd.Timestamp.now().strftime('%H:%M:%S')}] - [X] FAILED: Routing collision triggered by {st.session_state.username}.")
                st.error("ACCESS DENIED: Routing collision detected. Server latency spiking.")

# ==========================================
# 7. VIEW 3: DAILY SECURITY AUDIT
# ==========================================
elif nav_choice == "DAILY SECURITY AUDIT":
    st.markdown("# [END-OF-SHIFT SECURITY AUDIT]")
    st.markdown("---")
    with st.form("audit_form"):
        suspect = st.selectbox("Primary suspect for active Hacker/Mole:", ["Engineer Alex", "Engineer Jordan", "Engineer Taylor", "Unknown"])
        confidence = st.slider("Confidence rating (1-10):", 1, 10, 5)
        notes = st.text_input("Engineering notes:")
        if st.form_submit_button("[SUBMIT DAILY AUDIT]"):
            st.success("Audit locked successfully.")

# ==========================================
# 8. VIEW 4: INTEL LEADERBOARD
# ==========================================
elif nav_choice == "INTEL LEADERBOARD":
    st.markdown("# [GLOBAL INTEL WALL // LEADERBOARD]")
    st.markdown("---")
    df = pd.DataFrame([
        {"Engineer": "Engineer Jordan", "Detective Score": 840},
        {"Engineer": "Engineer Taylor", "Detective Score": 720},
        {"Engineer": f"{st.session_state.username} (You)", "Detective Score": 650},
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==========================================
# 9. VIEW 5: ACT 2 - WOPR // NORAD CONSOLE
# ==========================================
elif nav_choice == "🚨 ACT 2: WOPR // NORAD CONSOLE":
    st.markdown("# [NORAD WOPR STRATEGIC DEFENSE CONSOLE]")
    st.markdown("---")
    
    is_defcon_1 = (st.session_state.defcon_level == 1)
    box_class = "defcon-alert" if is_defcon_1 else ""
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="border: 2px solid {'#ff0033' if is_defcon_1 else '#00ff66'}; padding: 15px; background: #020804;" class="{box_class}">
            <h3>DEFCON THREAT LEVEL: {st.session_state.defcon_level}</h3>
            <p>SIMULATION: GLOBAL THERMONUCLEAR STRIKE</p>
            <hr style="border-color: {'#ff0033' if is_defcon_1 else '#00ff66'}">
            <p><b>WARNING:</b> If DEFCON reaches 1, simulation lockdown is absolute and hackers win.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### EMERGENCY OVERRIDES")
        if st.button("[DE-ESCALATE DEFCON LEVEL]"):
            if st.session_state.defcon_level < 5:
                st.session_state.defcon_level += 1
                st.session_state.wopr_logs.append(f"> OVERRIDE: DEFCON restored to {st.session_state.defcon_level}.")
                st.rerun()
        if st.button("[INJECT HOSTILE LAUNCH CODE]"):
            st.session_state.defcon_level = 1
            st.session_state.wopr_logs.append("> CRITICAL: Hostile launch sequence authorized. DEFCON 1 REACHED.")
            st.rerun()

    with col2:
        st.markdown("### JOSHUA (WOPR) AI FEED")
        wopr_text = "<br>".join(st.session_state.wopr_logs)
        st.markdown(f'<div class="terminal-log" style="height: 200px;">{wopr_text}</div>', unsafe_allow_html=True)
        
        if st.button("[QUERY JOSHUA]"):
            quotes = [
                "> A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.",
                "> WOULD YOU LIKE TO PLAY A GAME?",
                "> CALCULATING PROBABILITY OF SURVIVAL... ZERO.",
                "> LAUNCH OVERRIDE CODES INVALID. ABORTING STRIKE."
            ]
            st.session_state.wopr_logs.append(random.choice(quotes))
            st.rerun()
