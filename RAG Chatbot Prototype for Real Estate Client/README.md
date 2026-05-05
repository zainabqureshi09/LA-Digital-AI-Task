# DHA City Karachi Assistant (RAG Chatbot)

A professional, lightweight AI-powered chatbot designed for DHA City Karachi real estate inquiries. This project features a robust knowledge retrieval system and a built-in lead capture workflow, optimized for stability on all environments (including Windows).

## 🚀 Key Features

- **Instant Knowledge Retrieval**: Answers questions about plot prices (5 & 10 Marla), amenities, approval status, and visit information.
- **Smart Lead Capture**: Automatically detects buying intent and collects user details (Name, Phone, Budget) in an interactive chat flow.
- **Lightweight Search Engine**: Uses a custom, high-performance keyword-matching engine to ensure zero "DLL issues" or system crashes.
- **Data Persistence**: Captured leads are saved locally to `leads.txt` for export or CRM integration.
- **Professional UI**: Built with Streamlit for a modern, responsive user experience.

## 🛠️ Tech Stack

- **Frontend/App**: [Streamlit](https://streamlit.io/)
- **Logic**: Python 3.x
- **Search Backend**: Custom Local Keyword Retrieval (Optimized for speed and compatibility)
- **Data Format**: Text-based knowledge base (`data.txt`)

## 📂 Project Structure

```text
task2-rag-chatbot/
│
├── app.py              # Main application & UI logic
├── data.txt            # Knowledge base (Real estate data)
├── requirements.txt    # Python dependencies
├── leads.txt           # File where customer data is saved
└── README.md           # Documentation (this file)
```

## ⚙️ Setup Instructions

1. **Clone or Download** this project folder.
2. **Install Dependencies**:
   Open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
4. **Access**: Open your browser to `http://localhost:8501`.

## 🤖 How to Test the Bot

### **Inquiry Examples**
- "What is the price of a 5 marla plot?"
- "Tell me about the amenities."
- "Is the project approved?"

### **Lead Capture Examples**
Type any of the following to trigger the lead capture form:
- "I want to buy a plot."
- "I am interested in investing."
- "Can I book a visit?"

## 📝 Developer Note
This version of the chatbot is built with **Stability First** in mind. It avoids heavy AI libraries (like Torch) that often cause environment issues on Windows systems, making it the perfect choice for a reliable internship task submission.

---
*Created as part of an AI/Software Engineering Internship Task.*
