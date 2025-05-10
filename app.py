import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from pytrends.request import TrendReq

# Create a TrendReq session with spoofed headers
custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
pytrend = TrendReq(hl='en-US', tz=360, requests_args={'headers': custom_headers})

# Streamlit App Title
st.title("📊 Google Trends Explorer")

# Topic input
kw = st.text_input("Enter a topic to explore trends", "Taylor Swift")

# Cached region interest fetcher
@st.cache_data(ttl=3600)
def fetch_interest_by_region(keyword):
    pytrend.build_payload(kw_list=[keyword])
    time.sleep(2)  # avoid rate limiting
    return pytrend.interest_by_region()

# Cached trending searches
@st.cache_data(ttl=1800)
def fetch_today_searches():
    time.sleep(2)
    return pytrend.today_searches(pn='US')

# Cached suggestions
@st.cache_data(ttl=1800)
def fetch_suggestions(keyword):
    time.sleep(2)
    return pytrend.suggestions(keyword=keyword)

# Cached related queries
@st.cache_data(ttl=3600)
def fetch_related_queries(keyword):
    pytrend.build_payload([keyword])
    time.sleep(2)
    return pytrend.related_queries()

# Interest by Region
if st.button("Show Interest by Region"):
    try:
        df_region = fetch_interest_by_region(kw)
        top_regions = df_region.sort_values(by=kw, ascending=False).head(10)
        st.subheader("Top Regions by Interest")
        st.dataframe(top_regions)

        fig, ax = plt.subplots(figsize=(10, 5))
        top_regions.reset_index().plot(x='geoName', y=kw, kind='bar', ax=ax)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error fetching region data: {e}")

# Today's Trending Searches
if st.button("Show Today's Trending Searches (US)"):
    try:
        df_today = fetch_today_searches()
        st.subheader("🔥 Today's Trending Searches (US)")
        st.dataframe(df_today)
    except Exception as e:
        st.error(f"Error fetching trending searches: {e}")

# Keyword Suggestions
if st.button("Get Keyword Suggestions"):
    try:
        suggestions = fetch_suggestions(kw)
        df_suggestions = pd.DataFrame(suggestions).drop(columns='mid', errors='ignore')
        st.subheader("🧠 Suggested Keywords")
        st.dataframe(df_suggestions)
    except Exception as e:
        st.error(f"Error fetching suggestions: {e}")

# Related Queries
if st.button("Show Related Queries"):
    try:
        related = fetch_related_queries(kw)
        top = related[kw].get('top')
        rising = related[kw].get('rising')

        if top is not None:
            st.subheader("🔗 Top Related Queries")
            st.dataframe(top)
        else:
            st.info("No top related queries found.")

        if rising is not None:
            st.subheader("🚀 Rising Related Queries")
            st.dataframe(rising)
        else:
            st.info("No rising related queries found.")
    except Exception as e:
        st.error(f"Error fetching related queries: {e}")
