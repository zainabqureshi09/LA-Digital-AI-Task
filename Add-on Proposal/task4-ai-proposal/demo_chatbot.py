import time
import sys

def type_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def chatbot_demo():
    print("\n" + "="*50)
    print("      LA DIGITAL AGENCY - AI CHATBOT DEMO")
    print("="*50 + "\n")
    
    type_text("Bot: Hello! Welcome to our Real Estate portal. I'm your AI assistant.")
    type_text("Bot: How can I help you today?")
    print("\n(Simulated User input: 'I want to buy a plot')")
    time.sleep(1)
    
    type_text("\nBot: Great choice! I can certainly help you find the perfect plot.")
    type_text("Bot: To provide the best options, could you please share:")
    type_text("     1. Your Full Name")
    type_text("     2. Phone Number")
    type_text("     3. Your Estimated Budget (in PKR)")
    
    print("\n(Simulation: Gathering lead data...)")
    time.sleep(1.5)
    
    type_text("\nBot: Thank you! I've captured your requirements.")
    type_text("Bot: One of our senior sales executives will contact you within 5 minutes.")
    type_text("Bot: Would you like to book a site visit for this weekend?")
    
    print("\n" + "="*50)
    print("      LEAD CAPTURED & SYNCED TO GOOGLE SHEETS")
    print("="*50 + "\n")

if __name__ == "__main__":
    chatbot_demo()
