import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq

# config
st.set_page_config(page_title="AI Review Dashboard", layout="wide")

DATA_PATH = "/tmp/submissions.json"

def load_data():
    # Ensure file exists BEFORE reading
    if not os.path.isfile(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            f.write("[]")

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.markdown("""
<style>
/* ---------- Global ---------- */
.stApp {
    background: linear-gradient(180deg, #0b0f14 0%, #0e131a 100%);
    color: #e5e7eb;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: #0b0f14;
    border-right: 1px solid #1f2937;
}

/* Sidebar select */
[data-testid="stSidebar"] select {
    background-color: #111827 !important;
    color: #e5e7eb !important;
}

/* ---------- Headings ---------- */
h1, h2, h3 {
    color: #f9fafb;
    font-weight: 600;
}

/* ---------- Cards / Containers ---------- */
div[data-testid="stMetric"] {
    background: #0f172a;
    border-radius: 12px;
    padding: 16px;
}

/* ---------- Inputs ---------- */
textarea, input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border: 1px solid #1f2937 !important;
    border-radius: 8px !important;
}

/* Select box */
div[data-baseweb="select"] > div {
    background-color: #020617;
    color: #e5e7eb;
    border-radius: 8px;
}

/* ---------- Buttons ---------- */
.stButton > button {
    background-color: #f97316;
    color: #020617;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1.2rem;
}

.stButton > button:hover {
    background-color: #fb923c;
    color: #020617;
}

/* ---------- Dividers ---------- */
hr {
    border-color: #1f2937;
}

/* ---------- Review blocks ---------- */
.review-block {
    background: #020617;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}
/* ----- Fix white input container ----- */
div[data-testid="stSelectbox"],
div[data-testid="stTextArea"] {
    background-color: transparent !important;
}

/* Remove inner white box */
div[data-baseweb="base-input"] {
    background-color: #020617 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 10px !important;
}

/* ----- Highlight field labels ----- */
label {
    color: #f97316 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* ----- Improve placeholder contrast ----- */
textarea::placeholder,
input::placeholder {
    color: #9ca3af !important;
}

/* ----- Focus state (nice UX) ----- */
textarea:focus,
input:focus {
    outline: none !important;
    border-color: #f97316 !important;
    box-shadow: 0 0 0 1px rgba(249,115,22,0.4);
}
/* Metric value (big number) */
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700;
}

/* Metric label (Total Reviews / Average Rating) */
div[data-testid="stMetricLabel"] {
    color: #f97316 !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


def call_llm(prompt):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return completion.choices[0].message.content.strip()

# Prompts
USER_RESPONSE_PROMPT = """
You are a polite customer support assistant.
Write a short, empathetic response to this restaurant review:

"{review}"
"""

SUMMARY_PROMPT = """
Summarise the following restaurant review in one short sentence:

"{review}"
"""

ACTION_PROMPT = """
Based on the following restaurant review, suggest 1–2 concrete actions
the restaurant manager should take:

"{review}"
"""

# UI
st.title("Restaurant Review System")

view = st.sidebar.selectbox(
    "Select Dashboard",
    ["User Dashboard", "Admin Dashboard"]
)

#USER DASHBOARD 
if view == "User Dashboard":
    st.header("Submit a Review")

    rating = st.selectbox("Star Rating", [1, 2, 3, 4, 5])
    review = st.text_area("Your Review")

    if st.button("Submit"):
        if review.strip() == "":
            st.error("Please write a review.")
        else:
            ai_response = call_llm(
                USER_RESPONSE_PROMPT.format(review=review)
            )
            ai_summary = call_llm(
                SUMMARY_PROMPT.format(review=review)
            )
            ai_action = call_llm(
                ACTION_PROMPT.format(review=review)
            )

            data = load_data()
            data.append({
                "timestamp": datetime.utcnow().isoformat(),
                "rating": rating,
                "review": review,
                "ai_response": ai_response,
                "ai_summary": ai_summary,
                "ai_action": ai_action
            })
            save_data(data)

            st.success("Review submitted!")
            st.subheader("AI Response")
            st.write(ai_response)

# ADMIN DASHBOARD 
else:
    st.header("Admin Dashboard")

    data = load_data()

    if len(data) == 0:
        st.info("No reviews yet.")
    else:
        avg_rating = round(
            sum(d["rating"] for d in data) / len(data), 2
        )

        col1, col2 = st.columns(2)
        col1.metric("Total Reviews", len(data))
        col2.metric("Average Rating", avg_rating)

        st.divider()

        for d in reversed(data):
            st.write(f"⭐ Rating: {d['rating']}")
            st.write("**Review:**", d["review"])
            st.write("**AI Summary:**", d["ai_summary"])
            st.write("**Recommended Action:**", d["ai_action"])
            st.caption(d["timestamp"])
            st.divider()
