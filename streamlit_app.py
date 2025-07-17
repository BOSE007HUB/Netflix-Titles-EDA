import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# Title
st.title("Netflix Titles EDA Dashboard")
# Load dataset
df = pd.read_csv("netflix_titles.csv")
df.fillna({'country': 'Unknown', 'director': 'Unknown', 'cast': 'Unknown'}, inplace=True)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df['genre'] = df['listed_in'].str.split(', ')
# Sidebar Filter
st.sidebar.header("Filter")
selected_type = st.sidebar.selectbox("Content Type", options=["All", "Movie", "TV Show"])
if selected_type != "All":
    df = df[df['type'] == selected_type]
# Genre Plot
st.subheader(" Top 10 Genres")
genre_explode = df.explode('genre')
genre_count = genre_explode['genre'].value_counts().head(10).reset_index()
genre_count.columns = ['Genre', 'Count']
fig1 = px.bar(genre_count, x='Count', y='Genre', orientation='h', title='Top 10 Genres')
st.plotly_chart(fig1)
# Yearly Trend
st.subheader(" Yearly Trend of Content Release")
yearly = df['release_year'].value_counts().sort_index()
yearly_df = yearly.reset_index()
yearly_df.columns = ['Release Year', 'Count']
fig2 = px.line(yearly_df, x='Release Year', y='Count', title='Year-wise Release Trend')
st.plotly_chart(fig2)
# Country-wise
st.subheader("Top 10 Countries")
top_countries = df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['Country', 'Count']
fig3 = px.bar(top_countries, x='Country', y='Count', title='Top Countries by Content')
st.plotly_chart(fig3)
# Duration Analysis
st.subheader("Duration Analysis")
if selected_type == "Movie":
    df['duration_min'] = df['duration'].str.extract('(\d+)').astype(float)
    fig4 = px.histogram(df, x='duration_min', nbins=30, title='Movie Duration Distribution')
    st.plotly_chart(fig4)
elif selected_type == "TV Show":
    df['num_seasons'] = df['duration'].str.extract('(\d+)').astype(float)
    fig5 = px.histogram(df, x='num_seasons', nbins=10, title='TV Show Season Distribution')
    st.plotly_chart(fig5)
else:
    st.markdown("_Select content type to see specific duration analysis._")
