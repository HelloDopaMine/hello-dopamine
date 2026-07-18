import streamlit as st
import json
import pandas as pd
from dateutil import parser
from dateutil import tz

# Cohesive Calming Brand Configuration
st.set_page_config(page_title="Hello DopaMine Pro", page_icon="🧠", layout="wide")

# Custom CSS for Premium Sage/Slate Branding
st.markdown("""
    <style>
    .main { background-color: #1c2321; }
    h1 { color: #a9bba2 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    h2, h3, p, span { color: #f4f6f0 !important; }
    .stMetric { background-color: #2a3431; padding: 20px; border-radius: 12px; border: 1px solid #475853; }
    div[data-testid="stMetricValue"] { color: #e1e7dd !important; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #a9bba2 !important; }
    section[data-testid="stSidebar"] { background-color: #242c29 !important; border-right: 1px solid #323d39; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Hello DopaMine Pro")
st.subheader("The Ultimate Behavioral Psychology & YouTube Analyzer")
st.write("Isolate your algorithmic feedback loops, map attention variety decay, and recover executive control.")
st.markdown("---")

# Premium Conversions Sidebar
st.sidebar.markdown("### 🌟 Hello DopaMine Pro Pass")
st.sidebar.write("Unlock your full chronological velocity tracking, entropy index metrics, and a tailored screen-time correction schedule.")

PAYMENT_LINK = "https://buymeacoffee.com" 

st.sidebar.markdown(f'<a href="{PAYMENT_LINK}" target="_blank"><button style="width:100%; padding:12px; background-color:#5e7463; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer; font-size:16px;">Unlock Full Psychological Profile ($9)</button></a>', unsafe_allow_html=True)

# Secure File Uploader Pipeline (Only ONE box allowed!)
uploaded_file = st.file_uploader(label="⚡ Securely drag and drop your watch-history.json file here", type=["json"])

if uploaded_file is not None:
    st.success("🔒 Data packet parsed locally. Compiling initial behavioral vectors...")
    try:
        data = json.load(uploaded_file)
    except:
        st.error("❌ Failed to read JSON file. Make sure it is an unzipped watch-history.json file.")
        st.stop()
    
    titles, channels, search_queries, years = [], [], [], []
    local_zone = tz.tzlocal()

    for entry in data:
        if isinstance(entry, dict) and "titleUrl" in entry:
            if "title" in entry and entry["title"].startswith("Watched "):
                titles.append(entry["title"].replace("Watched ", "", 1))
                sub = entry.get("subtitles")
                if isinstance(sub, list) and len(sub) > 0:
                    c_name = sub[0].get("name") if isinstance(sub[0], dict) else None
                elif isinstance(sub, dict):
                    c_name = sub.get("name")
                else:
                    c_name = None
                if c_name: channels.append(c_name)
                if "time" in entry:
                    try: years.append(parser.isoparse(entry["time"]).astimezone(local_zone).year)
                    except: continue
            elif "title" in entry and entry["title"].startswith("Searched for "):
                query = entry["title"].replace("Searched for ", "", 1)
                if query.strip(): search_queries.append(query)

    # Core Metric Calculations
    total_videos = len(titles)
    est_hours = (total_videos * 11) / 60 
    
    # --- ROW 1: Summary Cards ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎬 Total Videos Audited", f"{total_videos:,}")
    col2.metric("⏳ Estimated Screen Hours", f"{est_hours:,.1f}")
    col3.metric("🎙️ Creators Encountered", f"{len(set(channels)):,}")
    col4.metric("🔍 Lifetime Search Indexes", f"{len(search_queries):,}")

    st.markdown("---")

    # --- ROW 2: Tables ---
    left, right = st.columns(2)
    with left:
        st.subheader("👑 Top 10 Most Interacted Channels")
        if channels:
            st.dataframe(pd.DataFrame(channels, columns=["Creator Channel"]).value_counts().reset_index(name="Watches").head(10), use_container_width=True, hide_index=True)
    with right:
        st.subheader("🔥 Top 10 Search Intent Triggers")
        if search_queries:
            st.dataframe(pd.DataFrame(search_queries, columns=["Query Keyword"]).value_counts().reset_index(name="Searches").head(10), use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # --- ROW 3: Chart ---
    st.subheader("📈 Chronological Consumption Footprint (Annual Scale)")
    if years:
        st.bar_chart(pd.DataFrame(years, columns=["Year"]).value_counts().reset_index(name="Count").sort_values("Year"), x="Year", y="Count", color="#a9bba2", use_container_width=True)

    # --- ROW 4: Premium Hooks ---
    st.markdown("---")
    st.subheader("🧠 Deep Psychological Loop Profile")
    
    lock_left, lock_right = st.columns(2)
    with lock_left:
        st.info("🔒 **[VECTOR 1] Binge Session Velocity Tracking**")
        st.write("• **Continuous Binge Loops Captured:** `LOCKED`")
        st.write("• **Max Interrupted Session Velocity:** `LOCKED` (Calculates the absolute maximum video count watched in a single sitting without a 30-minute break)")
        
    with lock_right:
        st.info("🔒 **[VECTOR 2] Attention Entropy Decay Traps**")
        st.write("• **Algorithmic Entrainment Rating:** `LOCKED`")
        st.write("• **Primary Creator Fixation Vector:** `LOCKED` (Pinpoints the exact channel loops that successfully bypassed your executive function control)")

    st.markdown("<br>", unsafe_allow_html=True)
    st.warning("⚠️ **Advanced Cognitive Metrics are Masked.** Upgrade to the Pro Pass in the left sidebar to generate your complete premium diagnostic text profile containing your Screen-Time Correction Schedule.")

else:
    st.info("💡 Standby. Securely drag and drop your JSON history file above to populate the interface dashboard matrices.")
