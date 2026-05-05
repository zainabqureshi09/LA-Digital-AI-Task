import streamlit as st
import os
import datetime
import re

# --- CONFIGURATION ---
LEADS_FILE = "leads.txt"
DATA_FILE = "data.txt"

st.set_page_config(page_title="DHA City Karachi Assistant", layout="centered", page_icon="🏙️")

# --- LEAD CAPTURE LOGIC ---
def save_lead(name, phone, budget):
    """Saves lead information into a local text file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LEADS_FILE, "a") as f:
        f.write(f"{name}, {phone}, {budget}, {timestamp}\n")

def check_intent(text):
    """Checks for buying/booking intent."""
    keywords = ["buy", "purchase", "invest", "book", "interested", "visit"]
    return any(kw in text.lower() for kw in keywords)

# --- LIGHTWEIGHT SEARCH ENGINE (No Torch Required) ---
def simple_search(query, data_path):
    """A lightweight keyword-based search to avoid heavy Torch/DLL issues."""
    if not os.path.exists(data_path):
        return "Knowledge base not found."
    
    with open(data_path, "r") as f:
        content = f.read()
    
    # Split content into sections (usually by double newline)
    sections = content.split('\n\n')
    
    # Simple keyword matching score
    query_words = set(re.findall(r'\w+', query.lower()))
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
    return "I'm sorry, I couldn't find specific information on that. Please try asking about prices, amenities, or visits."

# --- STREAMLIT UI ---
def main():
    st.title("🏙️ DHA City Karachi Assistant")
    st.info("💡 Light Mode: This version uses a fast, local keyword-search to ensure compatibility with your system.")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "collecting_lead" not in st.session_state:
        st.session_state.collecting_lead = False
    if "lead_step" not in st.session_state:
        st.session_state.lead_step = 0
    if "lead_data" not in st.session_state:
        st.session_state.lead_data = {}

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- LEAD CAPTURE WORKFLOW ---
    if st.session_state.collecting_lead:
        lead_questions = ["What is your full name?", "What is your phone number?", "What is your estimated budget for investment?"]
        current_step = st.session_state.lead_step
        
        if current_step < len(lead_questions):
            with st.chat_message("assistant"):
                st.markdown(lead_questions[current_step])
            
            if user_response := st.chat_input("Enter details..."):
                keys = ["name", "phone", "budget"]
                st.session_state.lead_data[keys[current_step]] = user_response
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.messages.append({"role": "assistant", "content": lead_questions[current_step]})
                st.session_state.lead_step += 1
                st.rerun()
        else:
            save_lead(st.session_state.lead_data["name"], st.session_state.lead_data["phone"], st.session_state.lead_data["budget"])
            with st.chat_message("assistant"):
                msg = "Thank you! Your information has been saved. Our representative will contact you shortly."
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state.collecting_lead = False
            st.session_state.lead_step = 0
            st.session_state.lead_data = {}
            st.rerun()
        return

    # --- REGULAR CHAT ---
    if prompt := st.chat_input("Ask about plot prices, amenities, or status..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if check_intent(prompt):
            with st.chat_message("assistant"):
                intro = "It sounds like you're interested in DHA City Karachi! I can help you with that. Could you please provide a few details so our team can reach out?"
                st.markdown(intro)
                st.session_state.messages.append({"role": "assistant", "content": intro})
                st.session_state.collecting_lead = True
                st.rerun()
        else:
            with st.chat_message("assistant"):
                answer = simple_search(prompt, DATA_FILE)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
