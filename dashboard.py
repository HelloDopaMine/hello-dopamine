import streamlit as st
import json
import pandas as pd
from dateutil import parser
from dateutil import tz

# Premium UI Configuration
st.set_page_config(page_title="Hello DopaMine Pro", page_icon="🚀", layout="wide")

# Custom CSS for Calming Brand Alignment
st.markdown("""
    <style>
    /* Main Web Background and Typography */
    .main { background-color: #1c2321; }
    h1 { color: #a9bba2 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    h2, h3, p, span { color: #f4f6f0 !important; }
    
    /* Premium Metric Blocks styling */
    .stMetric { background-color: #2a3431; padding: 20px; border-radius: 12px; border: 1px solid #475853; }
    div[data-testid="stMetricValue"] { color: #e1e7dd !important; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #a9bba2 !important; }
    
    /* Left Sidebar Styling Overrides */
    section[data-testid="stSidebar"] { background-color: #242c29 !important; border-right: 1px solid #323d39; }
    
    /* Clean Custom Button */
    div.stButton > button:first-child {
        background-color: #5e7463 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        transition: background-color 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #728c78 !important;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("🚀 Hello DopaMine Pro")
st.subheader("The Ultimate YouTube Habit & Productivity Analyzer")
st.write("Unlock hidden viewing metrics, optimize your screen time, and discover your true digital profile.")
st.markdown("---")

# Monetization Hook / Call to Action Sidebar
st.sidebar.markdown("### 🌟 Upgrade to Hello DopaMine Pro")
st.sidebar.write("Get deep AI-driven psychological watch-habit profiles, exportable CSV reports, and historical projections.")

# !!! PASTE YOUR COPIED BUY ME A COFFEE LINK IN THE QUOTES BELOW !!!
PAYMENT_LINK = "https://buymeacoffee.com/HelloDopaMine/e/557971" 

st.sidebar.markdown(f'<a href="{PAYMENT_LINK}" target="_blank"><button style="width:100%; padding:12px; background-color:#5e7463; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">Unlock Lifetime Pro Access ($9)</button></a>', unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader(label="⚡ Securely drag and drop your watch-history.json file here", type=["json"])

if uploaded_file is not None:
    st.success("🔒 Local data pipeline established. Generating analytics dashboard...")
    data = json.load(uploaded_file)
    
    titles, channels, search_queries, years = [], [], [], []
    local_zone = tz.tzlocal()

    for entry in data:
        if "titleUrl" in entry and "title" in entry:
            if entry["title"].startswith("Watched "):
                titles.append(entry["title"].replace("Watched ", "", 1))
                if "subtitles" in entry and len(entry["subtitles"]) > 0:
                    sub = entry["subtitles"]
                    # Fix a dictionary/list parsing crash bug
                    if isinstance(sub, list) and len(sub) > 0:
                        c_name = sub[0].get("name")
                    elif isinstance(sub, dict):
                        c_name = sub.get("name")
                    else:
                        c_name = None
                    if c_name: 
                        channels.append(c_name)
                if "time" in entry:
                    try: years.append(parser.isoparse(entry["time"]).astimezone(local_zone).year)
                    except: continue
        elif "title" in entry and entry["title"].startswith("Searched for "):
            query = entry["title"].replace("Searched for ", "", 1)
            if query.strip(): search_queries.append(query)

    # Metrics Display
    total_videos = len(titles)
    est_hours = (total_videos * 11) / 60 
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎬 Total Videos Watched", f"{total_videos:,}")
    col2.metric("⏳ Est. Hours Wasted", f"{est_hours:,.1f}")
    col3.metric("🎙️ Channels Discovered", f"{len(set(channels)):,}")
    col4.metric("🔍 Search Index Count", f"{len(search_queries):,}")

    st.markdown("---")

    # Layout Panels
    left, right = st.columns(2)
    with left:
        st.subheader("👑 Most Consumed Channels")
        if channels:
            st.dataframe(pd.DataFrame(channels, columns=["Creator Channel"]).value_counts().reset_index(name="Watches").head(10), use_container_width=True, hide_index=True)
    with right:
        st.subheader("🔥 Top Search Intent Vectors")
        if search_queries:
            st.dataframe(pd.DataFrame(search_queries, columns=["Query Keyword"]).value_counts().reset_index(name="Searches").head(10), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📈 Digital Footprint Over Time (Annual Scale)")
    if years:
        st.bar_chart(pd.DataFrame(years, columns=["Year"]).value_counts().reset_index(name="Count").sort_values("Year"), x="Year", y="Count", color="#a9bba2", use_container_width=True)

    # Locked Premium Feature Teaser
    st.markdown("---")
    st.subheader("🧠 Premium Psychological Profile Analytics (LOCKED)")
    st.info("🔒 Unlock Premium Access in the sidebar to reveal your ADHD attention span analysis, dopamine loop triggers, and screen-time correction schedule.")
