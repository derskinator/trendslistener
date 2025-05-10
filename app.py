import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from pytrends.request import TrendReq

# Random User-Agent headers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X)",
]
headers = {"User-Agent": random.choice(user_agents)}

# TrendReq with randomized headers
pytrend = TrendReq(hl='en-US', tz=360, requests_args={'headers': headers})

st.title("📊 Google Trends Explorer (Rate-Limit Safe)")

# Session state for keyword payload setup
if "payload_built" not in st.session_state:
    st.session_state.payload_built = False

kw = st.text_input("Enter a topic to explore trends", "Taylor Swift")

# Step 1: Build Payload
if st.button("Step 1: Build Payload"):
    try:
        pytrend.build_payload([kw])
        st.session_state.payload_built = True
        st.success("✅ Payload built successfully. Now run queries.")
    except Exception as e:
        st.error(f"Failed to build payload: {e}")
        st.session_state.payload_built = False

# Step 2: Interest by Region
if st.button("Interest by Region") and st.session_state.payload_built:
    try:
        time.sleep(3)
        df_region = pytrend.interest_by_region()
        top_regions = df_region.sort_values(by=kw, ascending=False).head(10)

        st.subheader("Top Regions by Interest")
        st.dataframe(top_regions)

        fig, ax = plt.subplots(figsize=(10, 5))
        top_regions.reset_index().plot(x='geoName', y=kw, kind='bar', ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error fetching interest by region: {e}")

# Trending searches (does not require payload)
if st.button("Today's Trending Searches (US)"):
    try:
        time.sleep(3)
        df_today = pytrend.today_searches(pn='US')
        st.subheader("🔥 Today's Trending Searches (US)")
        st.dataframe(df_today)
    except Exception as e:
        st.error(f"Error fetching trending searches: {e}")

# Keyword Suggestions (does not require payload)
if st.button("Keyword Suggestions"):
    try:
        time.sleep(3)
        suggestions = pytrend.suggestions(keyword=kw)
        df_suggestions = pd.DataFrame(suggestions).drop(columns='mid', errors='ignore')
        st.subheader("🧠 Suggested Keywords")
        st.dataframe(df_suggestions)
    except Exception as e:
        st.error(f"Error fetching suggestions: {e}")

# Related Queries (requires payload)
if st.button("Related Queries") and st.session_state.payload_built:
    try:
        time.sleep(3)
        related = pytrend.related_queries()
        top = related[kw].get('top')
        rising = related[kw].get('rising')

        if top is not None:
            st.subheader("🔗 Top Related Queries")
            st.dataframe(top)
        if rising is not None:
            st.subheader("🚀 Rising Related Queries")
            st.dataframe(rising)
    except Exception as e:
        st.error(f"Error fetching related queries: {e}")
