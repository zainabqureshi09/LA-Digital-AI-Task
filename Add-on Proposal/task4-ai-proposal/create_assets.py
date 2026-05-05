from PIL import Image, ImageDraw, ImageFont
import os

def create_mockup(filename, text_lines):
    # Create a simple mockup image
    img = Image.new('RGB', (800, 600), color=(240, 240, 240))
    d = ImageDraw.Draw(img)
    
    # Draw a browser-like header
    d.rectangle([0, 0, 800, 40], fill=(200, 200, 200))
    d.ellipse([10, 10, 25, 25], fill=(255, 95, 87))
    d.ellipse([35, 10, 50, 25], fill=(255, 189, 46))
    d.ellipse([60, 10, 75, 25], fill=(39, 201, 63))
    
    # Draw chat bubbles
    y = 80
    for i, line in enumerate(text_lines):
        is_user = "User:" in line
        color = (0, 122, 255) if is_user else (229, 229, 234)
        text_color = (255, 255, 255) if is_user else (0, 0, 0)
        align = 400 if is_user else 50
        
        # Simple bubble
        d.rounded_rectangle([align, y, align + 350, y + 60], radius=15, fill=color)
        d.text((align + 20, y + 20), line, fill=text_color)
        y += 80
        
    img.save(filename)

os.makedirs('task4-ai-proposal/screenshots', exist_ok=True)
create_mockup('task4-ai-proposal/screenshots/chatbot_demo.png', [
    "User: I want to buy a plot",
    "Bot: Great! Please share your name,",
    "phone number, and budget."
])

print("Mockup created successfully.")
