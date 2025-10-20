import streamlit as st
import requests
import os

# Use environment variable or default to localhost
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.title("Board Games — Price Overview")
st.caption(f"API endpoint: {API_BASE}")

with st.form("scrape_form"):
    url = st.text_input("Product URL to scrape")
    submit = st.form_submit_button("Scrape and save")
    if submit and url:
        try:
            resp = requests.post(f"{API_BASE}/api/scrape", json={"url": url})
            resp.raise_for_status()
            st.success("Saved: %s" % resp.json().get("name"))
        except Exception as e:
            st.error(f"Scrape failed: {e}")

try:
    resp = requests.get(f"{API_BASE}/api/games")
    resp.raise_for_status()
    games = resp.json()
except Exception:
    games = []

if st.button("Refresh list"):
    try:
        resp = requests.get(f"{API_BASE}/api/games")
        resp.raise_for_status()
        games = resp.json()
    except Exception as e:
        st.error(f"Failed to fetch games: {e}")

for g in games:
    cols = st.columns([1, 4, 2])
    if g.get("image_url"):
        cols[0].image(g["image_url"], width=80)
    cols[1].markdown(f"**{g.get('name')}**\n\n{g.get('url')}")
    cols[2].write(g.get("price"))
