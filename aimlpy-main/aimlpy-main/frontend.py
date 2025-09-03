import streamlit as st
import requests

API_URL = "http://localhost:8083"  # FastAPI backend

st.set_page_config(page_title="AI/ML Notes Recommender", layout="wide")

st.title("📘 AI/ML Notes Recommender")

# Trending notes
# Trending notes
st.header("🔥 Trending Notes")
try:
    res = requests.get(f"{API_URL}/recommendations/trending")
    if res.status_code == 200:
        notes = res.json()
        if isinstance(notes, list):
            for n in notes:
                if isinstance(n, dict):  # expected dict with title/content
                    st.write(f"📌 {n.get('title', 'Untitled')} — {n.get('content', '')[:100]}...")
                else:  # fallback if it's just a string
                    st.write(f"📌 {n}")
        else:
            st.info(str(notes))
    else:
        st.warning("Could not load trending notes")
except Exception as e:
    st.error(f"Error connecting to API: {e}")


# Personalized recommendations
st.header("⭐ Recommended for You")
user_id = st.text_input("Enter your User ID", value="1")
if st.button("Get Recommendations"):
    try:
        res = requests.get(f"{API_URL}/recommendations/notes", params={"user_id": user_id})
        if res.status_code == 200:
            recs = res.json()
            if recs:
                for r in recs:
                    st.success(f"✅ {r.get('title', 'Untitled')}")
            else:
                st.info("No recommendations found for this user.")
        else:
            st.error("Failed to fetch recommendations")
    except Exception as e:
        st.error(f"Error: {e}")

# Feedback
st.header("📝 Feedback")
note_id = st.text_input("Note ID for feedback", value="1")
feedback = st.radio("Did you find this useful?", ["Yes", "No"])
if st.button("Submit Feedback"):
    try:
        payload = {"note_id": int(note_id), "feedback": 1 if feedback == "Yes" else 0}
        res = requests.post(f"{API_URL}/recommendations/feedback", json=payload)
        if res.status_code == 200:
            st.success("Feedback submitted ✅")
        else:
            st.error("Failed to submit feedback")
    except Exception as e:
        st.error(f"Error: {e}")
