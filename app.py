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
                # Host login check using PIN 0612
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
                    
                    # Check if user is in the host's designated saboteur list
                    sab_list = [s.strip().lower() for s in game["designated_saboteurs"].split(",")]
                    if st.session_state.username.lower() in sab_list:
                        st.session_state.is_saboteur = True
                    else:
                        st.session_state.is_saboteur = False
                        
                    st.rerun()
            else:
                st.error("Please enter a name to continue.")
    with col2:
        st.info("Collaborate on server routing puzzles, cast daily accusations, and keep our startup infrastructure running smoothly.")
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

nav_options = ["MISSION CONTROL", "CLOUD ROUTING PUZZLE", "ACCUSATION & VOTING", "LEADERBOARD"]
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
        st.info("Your troublemaker toolkit is active. Use your secret controls below to inject glitches and test the team!")
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
            st.metric(label="SYSTEM STATUS", value="NOMINAL")

    st.markdown("### LIVE SHARED SERVER ACTIVITY FEED")
    log_html = "<br>".join(game["logs"])
    st.markdown(f'<div class="terminal-log">{log_html}</div>', unsafe_allow_html=True)

    # Saboteur Action Panel (Broadcasting live to all players)
    if st.session_state.is_saboteur:
        st.markdown("---")
        st.markdown("### 🤹 TROUBLEMAKER CONTROL PANEL (SECRET)")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("[TRIGGER: COFFEE SPILL ON SERVER RACK]"):
                game["system_integrity"] = max(10.0, game["system_integrity"] - 12.5)
                game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [!] GLITCH: Coffee spill reported near Node 2 by an unknown source. Integrity compromised.")
                st.success("Sabotage executed! Cluster health dropped for everyone.")
                st.rerun()
        with col_h2:
            if game["act_2_active"]:
                if st.button("[TRIGGER: ESCALATED IT ALERT]"):
                    if game["defcon_level"] > 1:
                        game["defcon_level"] -= 1
                        game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [!] ALERT: Threat level escalated to DEFCON {game['defcon_level']}.")
                        st.success("DEFCON escalated!")
                        st.rerun()
            else:
                if st.button("[TRIGGER: PUSH BAD PULL REQUEST]"):
                    game["system_integrity"] = max(10.0, game["system_integrity"] - 15.0)
                    game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [!] ERROR: Unauthorized breaking commit merged into main branch.")
                    st.success("Bad commit pushed! Team health dropped.")
                    st.rerun()

    # Host Playability Dashboard
    if st.session_state.username.upper() == "HOST":
        st.markdown("---")
        st.markdown("### 📋 HOST GAME PIPELINE & PLAYABILITY CHECK")
        pipeline_df = pd.DataFrame([
            {"Stage": "Act 1: Startup Routing Puzzle", "Status": "Active & Live", "Difficulty": "Direct Match (Easy)", "Playability": "100% Synchronized"},
            {"Stage": "Accusation & Voting Board", "Status": "Active & Live", "Difficulty": "Social Deduction", "Playability": "100% Real-Time"},
            {"Stage": "Act 2: WOPR DEFCON Escalation", "Status": "Ready in Sidebar", "Difficulty": "High Tension", "Playability": "Toggle Controlled"},
        ])
        st.dataframe(pipeline_df, use_container_width=True, hide_index=True)

# ==========================================
# 7. VIEW 2: CLOUD ROUTING PUZZLE
# ==========================================
elif nav_choice == "CLOUD ROUTING PUZZLE":
    st.markdown("# [TEAM PUZZLE // CLOUD ROUTING MATRIX]")
    st.markdown("---")
    st.markdown("""
    **Challenge:** A recent repository update scrambled our microservice routing table. Check the active server nodes below, read the deployment notes, and match each server to its correct service to restore team health!
    """)

    st.markdown("### 🖥️ ACTIVE SERVER NODES")
    server_df = pd.DataFrame([
        {"Region": "AWS US-East", "Status": "Scrambled", "Current Load": f"{round(100 - game['system_integrity'])}%"},
        {"Region": "GCP Europe", "Status": "Scrambled", "Current Load": f"{round(95 - game['system_integrity'])}%"},
        {"Region": "Azure Asia-South", "Status": "Scrambled", "Current Load": f"{round(90 - game['system_integrity'])}%"},
    ])
    st.dataframe(server_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("""
    **Deployment Notes:**
    1. AWS US-East runs the Auth Service Shard.
    2. GCP Europe houses the Billing API.
    3. Azure Asia-South runs the Redis Cache.
    """)
    
    with st.form("puzzle_form"):
        node_us = st.selectbox("AWS US-East Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"])
        node_eu = st.selectbox("GCP Europe Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"])
        node_asia = st.selectbox("Azure Asia-South Node runs:", ["Auth Service Shard", "Billing API", "Redis Cache", "AI Inference Engine"])
        
        submit_puzzle = st.form_submit_button("[VERIFY ROUTING FIX]")
        if submit_puzzle:
            if node_us == "Auth Service Shard" and node_eu == "Billing API" and node_asia == "Redis Cache":
                game["system_integrity"] = min(100.0, game["system_integrity"] + 20.0)
                game["team_score"] += 250
                game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [OK] Routing puzzle successfully restored by {st.session_state.username}.")
                st.success("GREAT JOB: Microservice architecture restored! +250 Points and Cluster Health repaired.")
            else:
                game["logs"].insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] - [X] MISMATCH: Routing error triggered by {st.session_state.username}.")
                st.error("NOT QUITE: Routing mismatch detected. Match the deployment notes directly!")

# ==========================================
# 8. VIEW 3: ACCUSATION & VOTING BOARD
# ==========================================
elif nav_choice == "ACCUSATION & VOTING":
    st.markdown("# [DAILY ACCUSATION & SUSPICION BOARD]")
    st.markdown("---")
    st.markdown("""
    Who do you think has been messing with the cluster logs and breaking builds? Cast your secret suspicion vote below and review where team suspicions lie!
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
        
        st.markdown("### EMERGENCY OVERRIDES")
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
