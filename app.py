import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="HYPERION CLOUD // TEAM GAME",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SHARED GLOBAL GAME STATE (REAL-TIME SYNC)
# ==========================================
@st.cache_resource
def get_shared_game_state():
    return {
        "team_score": 1250,
        "system_integrity": 88.4,
        "act_2_active": False,
        "defcon_level": 5,
        "designated_saboteurs": "Alex, Jordan",
        "votes": {},
        "solved_incidents": [],
        "logs": [
            "[09:00:12] - GITHUB HOOK: Main repository branch merged by @dev_lead.",
            "[10:14:20] - KUBERNETES POD: Cluster US-East autoscaled successfully.",
            "[11:05:00] - NOTICE: Minor latency spike detected on Redis cache node 3."
        ],
        "wopr_logs": [
            "> INITIALIZING NORAD DEFENSE LINK...",
            "> CONNECTION TO WOPR SUPERCOMPUTER ESTABLISHED.",
            "> GREETINGS. SHALL WE PLAY A GAME?"
        ]
    }

game = get_shared_game_state()

# Determine CSS theme based on Act 2 status
act_2_is_active = game["act_2_active"]
primary_color = "#00ff66" if act_2_is_active else "#ffb000"
bg_color = "#020804" if act_2_is_active else "#050505"
panel_bg = "#08140c" if act_2_is_active else "#111111"
border_color = "#00ff66" if act_2_is_active else "#332600"

st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .stApp {{
        background-color: {bg_color};
        color: {primary_color};
        font-family: 'Courier New', Courier, monospace;
    }}
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {{
        background-color: {panel_bg};
        border: 2px solid {border_color};
        border-left: 6px solid {primary_color};
        padding: 20px;
        border-radius: 0px;
        margin-bottom: 15px;
    }}
    
    h1, h2, h3 {{
        font-family: 'Courier New', Courier, monospace;
        color: {primary_color} !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
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
# 3. USER SESSION STATE
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "is_saboteur" not in st.session_state: st.session_state.is_saboteur = False

# ==========================================
# 4. AUTHENTICATION GATE
# ==========================================
if not st.session_state.logged_in:
    st.markdown("# [HYPERION CLOUD // TEAM PORTAL]")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### ENTER YOUR DETAILS TO JOIN")
        input_name = st.text_input("YOUR NAME / CODENAME:")
        input_pin = st.text_input("ACCESS PIN:", type="password")

        if st.button("CONNECT TO DASHBOARD"):
            name_clean = input_name.strip()
            if name_clean != "":
                # Host login verification using PIN 0612
                if name_clean.upper() == "HOST" and input_pin.strip() == "0612":
                    st.session_state.username = "HOST"
                    st.session_state.logged_in = True
                    st.session_state.is_saboteur = False
                    st.rerun()
                elif name_clean.upper() == "HOST":
                    st.error("ACCESS DENIED: Incorrect PIN for HOST.")
                else:
                    st.session_state.username = name_clean
                    st.session_state.logged_in = True
                    
                    # Check if user is in host's designated saboteur list
                    sab_list = [s.strip().lower() for s in game["designated_saboteurs"].split(",")]
                    if st.session_state.username.lower() in sab_list:
                        st.session_state.is_saboteur = True
                    else:
                        st.session_state.is_saboteur = False
                        
                    st.rerun()
            else:
                st.error("Please enter a name to continue.")
    with col2:
        st.info("Collaborate on live IT incident queues, cast daily accusations, and keep our startup infrastructure online.")
    st.stop()

# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown(f"### [USER: {st.session_state.username.upper()}]")
if st.session_state.is_saboteur:
    st.sidebar.warning("ROLE: [INSIDER TROUBLEMAKER]")
else:
    st.sidebar.success("ROLE: [SYSTEM ENGINEER]")

st.sidebar.markdown("---")

nav_options = ["MISSION CONTROL", "ACTIVE IT INCIDENTS (PUZZLES)", "ACCUSATION & VOTING", "LEADERBOARD"]
if game["act_2_active"]:
    nav_options.append("🚨 ACT 2: WOPR // NORAD CONSOLE")

nav_choice = st.sidebar.radio("NAVIGATION", nav_options)

st.sidebar.markdown("---")

# Host Controls in Sidebar
if st.session_state.username.upper() == "HOST":
    st.sidebar.markdown("### [HOST ADMIN PANEL]")
    game["designated_saboteurs"] = st.sidebar.text_input(
        "Saboteur Names (comma-separated):", 
        value=game["designated_saboteurs"]
    )
    
    host_act2_toggle = st.sidebar.toggle("ACTIVATE ACT 2 (WARGAMES FINALE)", value=game["act_2_active"])
    if host_act2_toggle != game["act_2_active"]:
        game["act_2_active"] = host_act2_toggle
        if host_act2_toggle:
            game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [!] CRITICAL: Server traffic dynamically rerouted to NORAD WOPR mainframe.")
        st.rerun()

if st.sidebar.button("LOG OUT"):
    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# 6. VIEW 1: MISSION CONTROL
# ==========================================
if nav_choice == "MISSION CONTROL":
    if game["act_2_active"]:
        st.markdown("# [NORAD DEFENSE // ACT 2 ACTIVE]")
        st.warning("⚠️ ALERT: Systems linked to military simulation. Threat escalation in progress.")
    elif st.session_state.is_saboteur:
        st.markdown("# [INSIDER CONSOLE // HYPERION CLOUD]")
        st.info("Your troublemaker toolkit is active. Use your secret controls below to disrupt active IT incidents and test the team!")
    else:
        st.markdown("# [HYPERION CLOUD // MISSION CONTROL]")
    
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="UPTIME FUND", value=f"{game['team_score']} PTS")
    with col2:
        st.metric(label="CLUSTER HEALTH", value=f"{round(game['system_integrity'], 1)}%")
    with col3:
        if game["act_2_active"]:
            status_label = "DEFCON 1 // CRITICAL" if game["defcon_level"] == 1 else f"DEFCON {game['defcon_level']}"
            st.metric(label="THREAT STATUS", value=status_label)
        else:
            resolved_count = len(game["solved_incidents"])
            st.metric(label="INCIDENTS RESOLVED", value=f"{resolved_count} / 3")

    st.markdown("### LIVE SHARED SERVER ACTIVITY FEED")
    log_html = "<br>".join(game["logs"])
    st.markdown(f'<div class="terminal-log">{log_html}</div>', unsafe_allow_html=True)

    # Saboteur Targetable Disruption Panel
    if st.session_state.is_saboteur:
        st.markdown("---")
        st.markdown("### 🤹 TROUBLEMAKER DISRUPTION PANEL (SECRET)")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("[DISRUPT: COFFEE SPILL ON SERVER RACK]"):
                game["system_integrity"] = max(10.0, game["system_integrity"] - 10.0)
                game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [!] GLITCH: Coffee spill reported near Node 2 by an unknown source.")
                st.success("Disruption sent! Cluster health dropped across all screens.")
                st.rerun()
        with col_h2:
            if game["act_2_active"]:
                st.info("💡 In Act 2, head to the **WOPR Console** tab to solve decryption riddles and lower DEFCON!")
            else:
                if st.button("[RE-SCRAMBLE A RESOLVED INCIDENT]"):
                    if game["solved_incidents"]:
                        removed = game["solved_incidents"].pop()
                        game["system_integrity"] = max(10.0, game["system_integrity"] - 15.0)
                        game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [!] ALERT: Sabotage detected! '{removed}' has been re-scrambled!")
                        st.success(f"Successfully re-scrambled {removed}!")
                        st.rerun()
                    else:
                        st.warning("No incidents have been resolved by the team yet to sabotage!")

    # Host Playability Dashboard
    if st.session_state.username.upper() == "HOST":
        st.markdown("---")
        st.markdown("### 📋 HOST GAME PIPELINE & PLAYABILITY CHECK")
        pipeline_df = pd.DataFrame([
            {"Stage": "Incident #1: Routing Matrix", "Status": "Active in Queue", "Difficulty": "Easy", "Playability": "Verified"},
            {"Stage": "Incident #2: SSL Cert Expiry", "Status": "Active in Queue", "Difficulty": "Medium", "Playability": "Verified"},
            {"Stage": "Incident #3: Memory Leak", "Status": "Active in Queue", "Difficulty": "Medium", "Playability": "Verified"},
            {"Stage": "Act 2: Saboteur Riddle Decryption", "Status": "Ready in WOPR", "Difficulty": "High Tension", "Playability": "Active for Insiders"},
        ])
        st.dataframe(pipeline_df, use_container_width=True, hide_index=True)

# ==========================================
# 7. VIEW 2: ACTIVE IT INCIDENTS (SERIES OF PUZZLES)
# ==========================================
elif nav_choice == "ACTIVE IT INCIDENTS (PUZZLES)":
    st.markdown("# [ACTIVE IT INCIDENT QUEUE]")
    st.markdown("---")
    st.markdown("""
    Work together as a team to diagnose and patch these active infrastructure failures. Each resolved incident restores cluster health and awards Uptime Points!
    """)

    # --- INCIDENT 1 ---
    with st.expander("🚨 INCIDENT #101: SCRAMBLED MICROSERVICE ROUTING MATRIX", expanded=("Routing Matrix" not in game["solved_incidents"])):
        if "Routing Matrix" in game["solved_incidents"]:
            st.success("✅ STATUS: RESOLVED AND PATCHED")
        else:
            st.markdown("**Deployment Notes:** Match each region to its correct service.")
            with st.form("puzzle_1"):
                node_us = st.selectbox("AWS US-East Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"], key="p1_us")
                node_eu = st.selectbox("GCP Europe Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"], key="p1_eu")
                node_asia = st.selectbox("Azure Asia-South Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"], key="p1_asia")
                
                if st.form_submit_button("[PATCH INCIDENT #101]"):
                    if node_us == "Auth Service Shard" and node_eu == "Billing API" and node_asia == "Redis Cache":
                        game["solved_incidents"].append("Routing Matrix")
                        game["system_integrity"] = min(100.0, game["system_integrity"] + 15.0)
                        game["team_score"] += 200
                        game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [OK] Incident #101 patched by {st.session_state.username}.")
                        st.rerun()
                    else:
                        st.error("Patch failed! Check deployment notes again.")

    # --- INCIDENT 2 ---
    with st.expander("🚨 INCIDENT #102: EXPIRED SSL SECURITY CERTIFICATE", expanded=("SSL Certificate" not in game["solved_incidents"])):
        if "SSL Certificate" in game["solved_incidents"]:
            st.success("✅ STATUS: RESOLVED AND PATCHED")
        else:
            st.markdown("**Security Alert:** The main load balancer certificate expired, causing browser warning screens for users.")
            with st.form("puzzle_2"):
                cert_choice = st.selectbox("Select the correct cryptographic protocol to deploy:", [
                    "TLS v1.0 (Legacy Standard)", 
                    "TLS v1.3 Secure Enclave Certificate", 
                    "Plaintext HTTP Unencrypted Bundle", 
                    "Self-Signed Test Certificate (Expired 2023)"
                ])
                if st.form_submit_button("[PATCH INCIDENT #102]"):
                    if "TLS v1.3" in cert_choice:
                        game["solved_incidents"].append("SSL Certificate")
                        game["system_integrity"] = min(100.0, game["system_integrity"] + 15.0)
                        game["team_score"] += 200
                        game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [OK] Incident #102 patched by {st.session_state.username}.")
                        st.rerun()
                    else:
                        st.error("Security audit rejected this certificate configuration!")

    # --- INCIDENT 3 ---
    with st.expander("🚨 INCIDENT #103: REDIS CACHE MEMORY LEAK", expanded=("Memory Leak" not in game["solved_incidents"])):
        if "Memory Leak" in game["solved_incidents"]:
            st.success("✅ STATUS: RESOLVED AND PATCHED")
        else:
            st.markdown("**Diagnostic Log:** One of our caching nodes is experiencing runaway memory allocation due to an infinite loop query.")
            with st.form("puzzle_3"):
                node_choice = st.selectbox("Select the faulty caching node to isolate and flush:", [
                    "Redis-Cache-Node-01 (Primary US)", 
                    "Redis-Cache-Node-02 (Backup EU)", 
                    "Redis-Cache-Node-03 (Orphaned Test Cluster)"
                ])
                if st.form_submit_button("[PATCH INCIDENT #103]"):
                    if "Node-03" in node_choice:
                        game["solved_incidents"].append("Memory Leak")
                        game["system_integrity"] = min(100.0, game["system_integrity"] + 20.0)
                        game["team_score"] += 300
                        game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [OK] Incident #103 patched by {st.session_state.username}.")
                        st.rerun()
                    else:
                        st.error("Flush failed! That node contains critical production data.")

# ==========================================
# 8. VIEW 3: ACCUSATION & VOTING BOARD
# ==========================================
elif nav_choice == "ACCUSATION & VOTING":
    st.markdown("# [DAILY ACCUSATION & SUSPICION BOARD]")
    st.markdown("---")
    st.markdown("""
    Who do you think keeps re-scrambling our resolved incidents and triggering server glitches? Cast your secret suspicion vote below!
    """)
    
    with st.form("voting_form"):
        suspect = st.selectbox("Cast your suspicion on:", ["Alex", "Jordan", "Taylor", "Morgan", "Unsure / Coincidence"])
        reason = st.text_input("Reasoning / Evidence:")
        if st.form_submit_button("[SUBMIT SUSPICION VOTE]"):
            game["votes"][st.session_state.username] = suspect
            st.success("Vote recorded on the secure board.")

    st.markdown("---")
    st.markdown("### 📊 LIVE SUSPICION TALLY")
    if game["votes"]:
        vote_df = pd.DataFrame(list(game["votes"].items()), columns=["Engineer", "Suspected Culprit"])
        st.dataframe(vote_df, use_container_width=True, hide_index=True)
    else:
        st.info("No votes cast yet. Be the first to accuse someone!")

# ==========================================
# 9. VIEW 4: LEADERBOARD
# ==========================================
elif nav_choice == "LEADERBOARD":
    st.markdown("# [TEAM INTEL LEADERBOARD]")
    st.markdown("---")
    df = pd.DataFrame([
        {"Engineer": "Colleague Jordan", "Detective Score": 840},
        {"Engineer": "Colleague Taylor", "Detective Score": 720},
        {"Engineer": f"{st.session_state.username} (You)", "Detective Score": 650},
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==========================================
# 10. VIEW 5: ACT 2 - WOPR // NORAD CONSOLE
# ==========================================
elif nav_choice == "🚨 ACT 2: WOPR // NORAD CONSOLE":
    st.markdown("# [NORAD WOPR STRATEGIC DEFENSE CONSOLE]")
    st.markdown("---")
    
    is_defcon_1 = (game["defcon_level"] == 1)
    box_class = "defcon-alert" if is_defcon_1 else ""
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="border: 2px solid {'#ff0033' if is_defcon_1 else '#00ff66'}; padding: 15px; background: #020804;" class="{box_class}">
            <h3>DEFCON THREAT LEVEL: {game["defcon_level"]}</h3>
            <p>SIMULATION: GLOBAL THERMONUCLEAR STRIKE</p>
            <hr style="border-color: {'#ff0033' if is_defcon_1 else '#00ff66'}">
            <p><b>WARNING:</b> If DEFCON reaches 1, simulation lockdown is absolute and the troublemakers win.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- SABOTEUR RIDDLE DECRYPTION TERMINAL ---
        if st.session_state.is_saboteur:
            st.markdown("---")
            st.markdown("### 🔓 SABOTEUR DECRYPTION RIDDLE TERMINAL")
            st.markdown("Solve tactical military riddles below to force DEFCON lower and secure victory for the insiders!")
            
            with st.form("saboteur_riddle_form"):
                riddle_choice = st.selectbox("Select Encryption Protocol:", [
                    "Protocol Alpha: What has to be broken before you can use it?",
                    "Protocol Beta: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
                    "Protocol Gamma: What is full of holes but still holds water?"
                ])
                answer_input = st.text_input("Enter Decryption Answer:")
                
                if st.form_submit_button("[SUBMIT DECRYPTION KEY]"):
                    ans = answer_input.strip().lower()
                    if ("egg" in ans and "Alpha" in riddle_choice) or \
                       ("echo" in ans and "Beta" in riddle_choice) or \
                       ("sponge" in ans and "Gamma" in riddle_choice):
                        if game["defcon_level"] > 1:
                            game["defcon_level"] -= 1
                            game["wopr_logs"].insert(0, f"> [!] OVERRIDE SUCCESSFUL: Saboteur decrypted launch vector. DEFCON dropped to {game['defcon_level']}.")
                            st.success("Decryption successful! DEFCON level dropped.")
                            st.rerun()
                        else:
                            st.warning("DEFCON is already at 1! Maximum threat achieved.")
                    else:
                        st.error("Decryption failed! Incorrect answer.")
        
        st.markdown("### EMERGENCY OVERRIDES (ENGINEERS)")
        if st.button("[RESTORE DEFCON LEVEL]"):
            if game["defcon_level"] < 5:
                game["defcon_level"] += 1
                game["wopr_logs"].insert(0, f"> OVERRIDE: DEFCON restored to {game['defcon_level']} by {st.session_state.username}.")
                st.rerun()
        if st.button("[TRIGGER SIMULATION DRILL]"):
            game["defcon_level"] = 1
            game["wopr_logs"].insert(0, "> CRITICAL: Hostile simulation drill initiated. DEFCON 1 REACHED.")
            st.rerun()

    with col2:
        st.markdown("### JOSHUA (WOPR) AI FEED")
        wopr_text = "<br>".join(game["wopr_logs"])
        st.markdown(f'<div class="terminal-log" style="height: 200px;">{wopr_text}</div>', unsafe_allow_html=True)
        
        if st.button("[QUERY JOSHUA]"):
            quotes = [
                "> A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.",
                "> WOULD YOU LIKE TO PLAY A GAME?",
                "> CALCULATING PROBABILITY OF SURVIVAL... ZERO.",
                "> LAUNCH OVERRIDE CODES INVALID. ABORTING STRIKE."
            ]
            game["wopr_logs"].insert(0, random.choice(quotes))
            st.rerun()
