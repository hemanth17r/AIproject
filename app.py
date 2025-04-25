import streamlit as st
import requests

# Updated OpenRouter API key
OPENROUTER_API_KEY = "open router key here"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def get_itinerary(destination, days, budget):
    prompt = (
        f"Create a personalized travel plan for {days} days to {destination} within a budget of ₹{budget}. "
        f"Include day-wise itinerary, local attractions, food suggestions, and travel tips."
    )
    
    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",  # Updated model
        "messages": [
            {"role": "system", "content": "You are a helpful travel planner."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Something went wrong:\n\n{e}"

st.set_page_config(page_title="AI Travel Companion", layout="centered")
st.title("✈️ AI Travel Companion")

with st.form("travel_form"):
    destination = st.text_input("Where do you want to go?")
    days = st.number_input("Number of days", min_value=1, max_value=30, value=5)
    budget = st.number_input("Budget in ₹ (INR)", min_value=1000, value=20000)
    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    if not destination:
        st.warning("Please enter a destination.")
    elif not OPENROUTER_API_KEY or "your_openrouter_api_key_here" in OPENROUTER_API_KEY:
        st.error("Please set your OpenRouter API key in the code or as an environment variable.")
    else:
        with st.spinner("Planning your trip..."):
            itinerary = get_itinerary(destination, days, budget)
            st.subheader("🗺️ Your Personalized Itinerary")
            st.markdown(itinerary)
