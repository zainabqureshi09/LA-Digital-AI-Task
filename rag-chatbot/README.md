# DHA City Karachi RAG Chatbot

A professional AI-powered chatbot designed for DHA City Karachi real estate inquiries. This project uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions based on a local knowledge base and captures potential customer leads.

## Features

- **AI Chatbot**: Answers questions about plot prices, amenities, and approval status.
- **RAG Pipeline**: Uses LangChain, FAISS, and Sentence-Transformers for efficient information retrieval.
- **Lead Capture**: Automatically detects buying intent and collects user details (Name, Phone, Budget).
- **Streamlit UI**: Clean, interactive web interface for a seamless user experience.
- **Local Storage**: Leads are saved to `leads.txt` for easy access.

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain](https://www.langchain.com/)
- **Vector Database**: [FAISS](https://github.com/facebookresearch/faiss)
- **Embeddings**: [HuggingFace (sentence-transformers)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- **Language Model**: [HuggingFace Hub (google/flan-t5-large)](https://huggingface.co/google/flan-t5-large)

## Project Structure

```text
task2-rag-chatbot/
│
├── app.py              # Main Streamlit application
├── data.txt            # Knowledge base (Real estate info)
├── requirements.txt    # Python dependencies
├── leads.txt           # Captured user leads
└── README.md           # Setup instructions
```

## Setup Instructions

1. **Clone or Download** the project folder.
2. **Install Dependencies**:
   Open your terminal and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Get a HuggingFace Token (Optional but Recommended)**:
   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens).
   - Create a "Read" token.
   - You can enter this token in the sidebar of the app to enable AI-generated responses.
4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## How it Works

1. **Knowledge Retrieval**: When you ask a question, the system searches `data.txt` for the most relevant information using vector similarity.
2. **AI Generation**: If a HuggingFace token is provided, the AI uses the retrieved context to generate a natural response. If not, it shows the matching text directly.
3. **Intent Detection**: If you say something like "I want to buy a plot", the chatbot switches to "Lead Capture Mode" to ask for your contact details.
4. **Data Persistence**: All leads are stored locally in `leads.txt`.

## Sample Questions to Try

- "What is the price of a 5 marla plot?"
- "Is DHA City Karachi approved?"
- "What amenities do you offer?"
- "Can I book a visit?"
- "I want to buy a plot" (to trigger lead capture)

---
*Created as part of an AI Engineering Internship task.*
