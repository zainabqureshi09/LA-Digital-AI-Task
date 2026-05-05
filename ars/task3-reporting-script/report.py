import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

# --- 1. CONFIGURATION ---
INPUT_FILE = 'data.csv'
CHART_FILE = 'chart.png'
PDF_FILE = 'report.pdf'

def generate_report():
    print("Starting report generation...")

    # --- 2. LOAD AND PROCESS DATA ---
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Calculate Metrics
    df['CTR (%)'] = (df['Clicks'] / df['Impressions']) * 100
    df['Cost Per Lead'] = df['Spend'] / df['Leads']

    # Aggregated Data
    total_spend = df['Spend'].sum()
    total_impressions = df['Impressions'].sum()
    total_clicks = df['Clicks'].sum()
    total_leads = df['Leads'].sum()
    avg_ctr = df['CTR (%)'].mean()
    avg_cpl = df['Cost Per Lead'].mean()

    print("Data processed successfully.")

    # --- 3. CREATE CHART ---
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Leads'], marker='o', label='Leads', color='blue')
    plt.plot(df['Date'], df['Clicks'] / 10, marker='s', label='Clicks (scaled /10)', color='green')
    plt.title('Daily Performance (Clicks vs Leads)')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()
    print(f"Chart saved as {CHART_FILE}")

    # --- 4. GENERATE PDF ---
    doc = SimpleDocTemplate(PDF_FILE, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Title Style
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor("#2E5077")
    )

    elements = []

    # Title
    elements.append(Paragraph("Digital Marketing Performance Report", title_style))
    elements.append(Spacer(1, 12))

    # Summary Section
    summary_data = [
        ["Metric", "Value"],
        ["Total Spend", f"${total_spend:,.2f}"],
        ["Total Impressions", f"{total_impressions:,}"],
        ["Total Clicks", f"{total_clicks:,}"],
        ["Total Leads", f"{total_leads:,}"],
        ["Average CTR", f"{avg_ctr:.2f}%"],
        ["Average Cost Per Lead", f"${avg_cpl:,.2f}"]
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E5077")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Performance Summary", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(summary_table)
    elements.append(Spacer(1, 30))

    # Chart Section
    elements.append(Paragraph("Performance Trends", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(Image(CHART_FILE, width=400, height=240))
    elements.append(Spacer(1, 30))

    # Detailed Table Section
    elements.append(Paragraph("Daily Detailed Data", styles['Heading2']))
    elements.append(Spacer(1, 10))
    
    # Prepare table data from DataFrame
    table_header = ["Date", "Spend", "Clicks", "Leads", "CTR (%)", "CPL"]
    table_rows = [table_header]
    for _, row in df.iterrows():
        table_rows.append([
            row['Date'],
            f"${row['Spend']:,.2f}",
            f"{int(row['Clicks'])}",
            f"{int(row['Leads'])}",
            f"{row['CTR (%)']:.2f}%",
            f"${row['Cost Per Lead']:,.2f}"
        ])

    detailed_table = Table(table_rows, colWidths=[80, 80, 80, 80, 80, 80])
    detailed_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    
    elements.append(detailed_table)

    # Build PDF
    doc.build(elements)
    print(f"Report successfully generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_report()
