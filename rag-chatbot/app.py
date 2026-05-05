import streamlit as st
import os
import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

# --- CONFIGURATION ---
# These files store our knowledge base and lead information
LEADS_FILE = "leads.txt"
DATA_FILE = "data.txt"

# Set up the Streamlit page layout and title
st.set_page_config(page_title="DHA City Karachi Assistant", layout="centered", page_icon="🏙️")

# --- LEAD CAPTURE LOGIC ---
def save_lead(name, phone, budget):
    """Saves lead information into a local text file with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LEADS_FILE, "a") as f:
        # Appending data in a CSV-like format
        f.write(f"{name}, {phone}, {budget}, {timestamp}\n")

def check_intent(text):
    """Checks if the user's message indicates interest in buying or booking."""
    keywords = ["buy", "purchase", "invest", "book", "interested", "visit"]
    return any(kw in text.lower() for kw in keywords)

# --- RAG (Retrieval-Augmented Generation) PIPELINE ---
@st.cache_resource
def setup_rag():
    """Initializes the FAISS vector database from the local data.txt file."""
    if not os.path.exists(DATA_FILE):
        return None
    
    # 1. Load the knowledge base
    with open(DATA_FILE, "r") as f:
        raw_text = f.read()
    
    # 2. Split text into smaller chunks for better search results
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(raw_text)
    
    # 3. Create embeddings (converts text into numerical vectors)
    # Using a popular open-source model from HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 4. Create and return the FAISS vector store
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore

def get_answer(query, vectorstore):
    """Retrieves relevant context and generates an answer using an AI model."""
    
    # Define how the AI should behave
    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer concise and professional.

    {context}

    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # Check if HuggingFace token is available in environment
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    
    if hf_token:
        # Using a free model from HuggingFace Hub (FLAN-T5)
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-large", 
            model_kwargs={"temperature": 0.5, "max_length": 512},
            huggingfacehub_api_token=hf_token
        )
        
        # RetrievalQA connects the vector store and the LLM
        qa = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT}
        )
        result = qa.invoke(query)
        return result["result"]
    else:
        # Fallback: If no API token, just show the most relevant paragraph from data.txt
        docs = vectorstore.similarity_search(query)
        context = "\n".join([doc.page_content for doc in docs])
        return f" (Note: API Token missing. Showing matching info from Knowledge Base:)\n\n{context}"

# --- STREAMLIT UI ---
def main():
    st.title("🏙️ DHA City Karachi Assistant")
    st.markdown("Welcome! I'm here to help you with information about plots, amenities, and bookings in DHA City Karachi.")

    # Sidebar for HuggingFace Token (to enable AI generation)
    with st.sidebar:
        st.header("🔑 Setup")
        api_token = st.text_input("HuggingFace Hub Token (Optional)", type="password", help="Enter your HF token to enable AI chat.")
        if api_token:
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_token
            st.success("Token activated!")
        else:
            st.info("Without a token, the bot will show direct matches from the data file.")

    # Initialize session state variables for chat history and lead capture
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "collecting_lead" not in st.session_state:
        st.session_state.collecting_lead = False
    if "lead_step" not in st.session_state:
        st.session_state.lead_step = 0
    if "lead_data" not in st.session_state:
        st.session_state.lead_data = {}

    # Initialize the RAG system
    vectorstore = setup_rag()

    # Display chat history on every rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- LEAD CAPTURE WORKFLOW ---
    # This section runs if we are in the middle of asking for Name, Phone, or Budget
    if st.session_state.collecting_lead:
        lead_questions = ["What is your full name?", "What is your phone number?", "What is your estimated budget for investment?"]
        current_step = st.session_state.lead_step
        
        if current_step < len(lead_questions):
            with st.chat_message("assistant"):
                st.markdown(lead_questions[current_step])
            
            # Use chat_input to get the next detail
            if user_response := st.chat_input("Enter details here..."):
                # Store the data
                keys = ["name", "phone", "budget"]
                st.session_state.lead_data[keys[current_step]] = user_response
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.messages.append({"role": "assistant", "content": lead_questions[current_step]})
                
                # Move to next question
                st.session_state.lead_step += 1
                st.rerun()
        else:
            # All info collected! Save it.
            save_lead(
                st.session_state.lead_data["name"],
                st.session_state.lead_data["phone"],
                st.session_state.lead_data["budget"]
            )
            with st.chat_message("assistant"):
                success_msg = "Thank you! Your information has been saved. Our representative will contact you shortly."
                st.markdown(success_msg)
                st.session_state.messages.append({"role": "assistant", "content": success_msg})
            
            # Reset lead capture state
            st.session_state.collecting_lead = False
            st.session_state.lead_step = 0
            st.session_state.lead_data = {}
            st.rerun()
        return

    # --- REGULAR CHAT INPUT ---
    if prompt := st.chat_input("Ask about prices, amenities, or approval status..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Trigger Lead Capture if user shows buying intent
        if check_intent(prompt) and not st.session_state.collecting_lead:
            with st.chat_message("assistant"):
                intro = "It sounds like you're interested in booking! I can help with that. Could you please provide a few details so we can assist you better?"
                st.markdown(intro)
                st.session_state.messages.append({"role": "assistant", "content": intro})
                st.session_state.collecting_lead = True
                st.rerun()
        else:
            # Generate and show RAG answer
            with st.chat_message("assistant"):
                if vectorstore:
                    with st.spinner("Searching knowledge base..."):
                        answer = get_answer(prompt, vectorstore)
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Error: Knowledge base (data.txt) is missing.")

if __name__ == "__main__":
    main()
