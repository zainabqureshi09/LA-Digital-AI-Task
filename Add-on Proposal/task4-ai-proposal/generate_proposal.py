from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

def add_slide(prs, title_text, content_text=None, layout_index=1):
    slide_layout = prs.slide_layouts[layout_index]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = title_text
    
    if content_text:
        body_shape = slide.placeholders[1]
        tf = body_shape.text_frame
        tf.text = content_text
    return slide

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def main():
    prs = Presentation()

    # Define Colors
    NAVY = RGBColor(0, 32, 96)
    WHITE = RGBColor(255, 255, 255)
    GRAY = RGBColor(128, 128, 128)

    # 1. Cover Page
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    set_slide_background(slide, NAVY)
    
    title = slide.shapes.title
    title.text = "AI Chatbot for Lead Generation"
    title.text_frame.paragraphs[0].font.color.rgb = WHITE
    title.text_frame.paragraphs[0].font.size = Pt(44)
    title.text_frame.paragraphs[0].font.bold = True

    subtitle = slide.placeholders[1]
    subtitle.text = "Prepared for Marketing Clients by LA Digital Agency"
    subtitle.text_frame.paragraphs[0].font.color.rgb = WHITE
    subtitle.text_frame.paragraphs[0].font.size = Pt(24)

    # 2. Problem Statement
    slide = add_slide(prs, "Problem Statement", 
                     "• Slow customer response times\n"
                     "• Lost leads from websites and social media\n"
                     "• Manual handling of customer inquiries\n"
                     "• Low conversion rates due to delayed engagement")

    # 3. Solution Overview
    slide = add_slide(prs, "Solution Overview", 
                     "Our AI Chatbot acts as your 24/7 Digital Sales Assistant:\n\n"
                     "• Automatically responds to visitors instantly\n"
                     "• Captures lead information without human intervention\n"
                     "• Qualifies leads by budget and interest level\n"
                     "• Hands off high-quality leads to your sales team in real-time")

    # 4. Key Features
    slide = add_slide(prs, "Key Features", 
                     "• Instant AI Replies\n"
                     "• Smart Lead Capture Forms\n"
                     "• Budget & Interest Qualification\n"
                     "• WhatsApp & Website Integration\n"
                     "• CRM & Google Sheets Sync\n"
                     "• Automated Appointment Booking")

    # 5. Sample Chatbot Demo
    slide = add_slide(prs, "Sample Chatbot Demo")
    # Add mockup image
    img_path = 'task4-ai-proposal/screenshots/chatbot_demo.png'
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1), Inches(1.5), height=Inches(5))
    else:
        # Fallback text
        body = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3))
        body.text = "User: 'I want to buy a plot'\nBot: 'Great! Please share your name, phone number, and budget.'"

    # 6. Pricing
    slide = add_slide(prs, "Investment Plan")
    table_placeholder = slide.shapes.add_table(3, 2, Inches(1), Inches(2), Inches(8), Inches(2.5)).table
    table_placeholder.columns[0].width = Inches(5)
    table_placeholder.columns[1].width = Inches(3)
    
    table_placeholder.cell(0, 0).text = "Service Item"
    table_placeholder.cell(0, 1).text = "Investment (PKR)"
    table_placeholder.cell(1, 0).text = "One-time Setup Fee"
    table_placeholder.cell(1, 1).text = "80,000"
    table_placeholder.cell(2, 0).text = "Monthly Maintenance & AI Usage"
    table_placeholder.cell(2, 1).text = "25,000 / mo"

    # 7. ROI / Benefits
    slide = add_slide(prs, "ROI & Business Benefits", 
                     "• 30% Increase in Lead Volume\n"
                     "• 90% Faster Response Times\n"
                     "• 50% Reduction in Manual Qualifying Work\n"
                     "• Higher Conversion Rates from Web Traffic\n"
                     "• Superior Customer Experience")

    # 8. Tech Stack
    slide = add_slide(prs, "Advanced Tech Stack", 
                     "• Python & Streamlit (Core Engine)\n"
                     "• LangChain (LLM Orchestration)\n"
                     "• OpenAI API (Natural Language Understanding)\n"
                     "• FAISS (Vector Store for Knowledge Base)\n"
                     "• Google Sheets API (Data Storage)")

    # 9. Implementation Timeline
    slide = add_slide(prs, "Project Timeline")
    # Simple bullet points for timeline
    tf = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3)).text_frame
    p1 = tf.add_paragraph()
    p1.text = "Day 1-2: Development & Customization"
    p2 = tf.add_paragraph()
    p2.text = "Day 3: Intensive Testing & Refinement"
    p3 = tf.add_paragraph()
    p3.text = "Day 4: Final Deployment & Live Integration"

    # 10. Final Thank You Page
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    set_slide_background(slide, NAVY)
    
    title = slide.shapes.title
    title.text = "Thank You!"
    title.text_frame.paragraphs[0].font.color.rgb = WHITE
    
    subtitle = slide.placeholders[1]
    subtitle.text = "Contact LA Digital Agency to get started.\nEmail: info@ladigital.agency | Web: www.ladigital.agency"
    subtitle.text_frame.paragraphs[0].font.color.rgb = WHITE

    prs.save('task4-ai-proposal/proposal.pptx')
    print("Proposal generated successfully: task4-ai-proposal/proposal.pptx")

if __name__ == "__main__":
    main()
