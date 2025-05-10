import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt

# Setup
pytrend = TrendReq()

# Streamlit Interface
st.title("🌍 Google Trends Explorer")

# Keyword Input
kw = st.text_input("Enter a topic (e.g., 'Taylor Swift', 'AI')", "Taylor Swift")

# Search Interest by Region
if st.button("Show Interest by Region"):
    pytrend.build_payload(kw_list=[kw])
    df_region = pytrend.interest_by_region()
    top_regions = df_region.sort_values(by=kw, ascending=False).head(10)
    st.write("Top Regions by Search Interest:")
    st.dataframe(top_regions)

    # Bar Plot
    st.write("🔎 Visual Representation")
    fig, ax = plt.subplots(figsize=(10, 5))
    top_regions.reset_index().plot(x='geoName', y=kw, kind='bar', ax=ax)
    st.pyplot(fig)

# Daily Trending Searches
if st.button("Today's Trending Searches (US)"):
    df_daily = pytrend.today_searches(pn='US')
    st.write("📈 Trending Searches Today in the US:")
    st.dataframe(df_daily)

# Keyword Suggestions
if st.button("Keyword Suggestions"):
    suggestions = pytrend.suggestions(keyword=kw)
    df_suggestions = pd.DataFrame(suggestions).drop(columns='mid')
    st.write("🧠 Related Keyword Suggestions:")
    st.dataframe(df_suggestions)

# Related Queries
if st.button("Related Queries"):
    pytrend.build_payload([kw])
    related = pytrend.related_queries()
    top = related[kw]['top']
    rising = related[kw]['rising']
    st.write("🔗 Top Related Queries:")
    st.dataframe(top)
    st.write("🚀 Rising Related Queries:")
    st.dataframe(rising)
