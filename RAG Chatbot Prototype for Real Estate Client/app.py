import streamlit as st
import os
import datetime
import re
import random

# --- CONFIGURATION ---
LEADS_FILE = "leads.txt"
DATA_FILE = "data.txt"

st.set_page_config(
    page_title="DHA City Karachi Assistant",
    layout="centered",
    page_icon="🏙️"
)

# --- LEAD SAVE ---
def save_lead(name, phone, budget):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LEADS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name}, {phone}, {budget}, {timestamp}\n")


# --- INTENT CHECK ---
def check_intent(text):
    keywords = ["buy", "purchase", "invest", "book", "interested", "visit"]
    return any(kw in text.lower() for kw in keywords)


# --- SEARCH ENGINE ---
def simple_search(query, data_path):

    query = query.lower().strip()

    # ✅ GREETING FIX
    if query in ["hi", "hello", "hey", "salam", "assalam o alaikum"]:
        return random.choice([
            "👋 Hello! Welcome to DHA City Karachi Assistant.",
            "🏙️ Hi! Ask me about plots, prices, or booking details.",
            "Hello! I can help you with investment options in DHA City Karachi."
        ])

    if not os.path.exists(data_path):
        return "Knowledge base not found."

    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = content.split("\n\n")

    query_words = set(re.findall(r'\w+', query))
    best_match = ""
    max_score = 0

    for section in sections:
        section_words = set(re.findall(r'\w+', section.lower()))
        score = len(query_words.intersection(section_words))

        if score > max_score:
            max_score = score
            best_match = section

    if max_score > 0:
        return best_match

    return "🤔 I couldn't find exact info. Try asking about prices, location, or booking process."


# --- UI ---
def main():
    st.title("🏙️ DHA City Karachi Assistant")
    st.info("Light AI demo using keyword search + lead capture system")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "collecting_lead" not in st.session_state:
        st.session_state.collecting_lead = False

    if "lead_step" not in st.session_state:
        st.session_state.lead_step = 0

    if "lead_data" not in st.session_state:
        st.session_state.lead_data = {}

    # chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- LEAD FLOW ---
    if st.session_state.collecting_lead:
        questions = [
            "What is your full name?",
            "What is your phone number?",
            "What is your budget?"
        ]

        step = st.session_state.lead_step

        if step < len(questions):
            with st.chat_message("assistant"):
                st.markdown(questions[step])

            if user_input := st.chat_input("Type here..."):
                keys = ["name", "phone", "budget"]

                st.session_state.lead_data[keys[step]] = user_input

                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": questions[step]})

                st.session_state.lead_step += 1
                st.rerun()

        else:
            save_lead(
                st.session_state.lead_data["name"],
                st.session_state.lead_data["phone"],
                st.session_state.lead_data["budget"]
            )

            msg = "✅ Thank you! Our team will contact you soon."
            with st.chat_message("assistant"):
                st.markdown(msg)

            st.session_state.messages.append({"role": "assistant", "content": msg})

            st.session_state.collecting_lead = False
            st.session_state.lead_step = 0
            st.session_state.lead_data = {}
            st.rerun()

        return

    # --- CHAT ---
    if prompt := st.chat_input("Ask about plots, prices, or booking..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # intent detection
        if check_intent(prompt):

            reply = "🏙️ It looks like you're interested in investment. Please share details so our team can contact you."

            with st.chat_message("assistant"):
                st.markdown(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})

            st.session_state.collecting_lead = True
            st.rerun()

        else:
            answer = simple_search(prompt, DATA_FILE)

            with st.chat_message("assistant"):
                st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()