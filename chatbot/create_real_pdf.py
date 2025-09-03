#!/usr/bin/env python3
"""
Create a real PDF file for RAG testing
"""

from fpdf import FPDF

def create_wolf_ai_catalog_pdf():
    """Create a proper PDF file with Wolf AI product catalog"""
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Title
    pdf.cell(0, 10, "WOLF AI BUSINESS INTELLIGENCE SUITE 2024", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "PRODUCT CATALOG AND PRICING GUIDE", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    
    # Product 1: Strategic Planning Assistant
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Strategic Planning Assistant", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, "Monthly Subscription: $299", ln=True)
    pdf.cell(0, 6, "AI-powered strategic planning and market analysis tool", ln=True)
    pdf.cell(0, 6, "Key Features:", ln=True)
    pdf.cell(0, 5, "  - SWOT analysis automation", ln=True)
    pdf.cell(0, 5, "  - Competitive intelligence gathering", ln=True)
    pdf.cell(0, 5, "  - Strategic goal tracking and monitoring", ln=True)
    pdf.cell(0, 5, "  - Market research integration", ln=True)
    pdf.cell(0, 6, "Target Customers: Strategic consultants, mid-market companies", ln=True)
    pdf.cell(0, 6, "Expected ROI: 40% improvement in strategic planning efficiency", ln=True)
    pdf.ln(8)
    
    # Product 2: Financial Analytics Pro
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Financial Analytics Pro", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, "Monthly Subscription: $499", ln=True)
    pdf.cell(0, 6, "Advanced financial modeling and forecasting platform", ln=True)
    pdf.cell(0, 6, "Key Features:", ln=True)
    pdf.cell(0, 5, "  - ROI calculation and analysis", ln=True)
    pdf.cell(0, 5, "  - Budget planning and optimization", ln=True)
    pdf.cell(0, 5, "  - Financial reporting automation", ln=True)
    pdf.cell(0, 5, "  - Cash flow analysis and projections", ln=True)
    pdf.cell(0, 6, "Target Market: CFOs, financial analysts, investment firms", ln=True)
    pdf.cell(0, 6, "Business Benefits: Reduces financial analysis time by 60%", ln=True)
    pdf.ln(8)
    
    # Product 3: Market Intelligence Dashboard
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Market Intelligence Dashboard", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, "Monthly Subscription: $199", ln=True)
    pdf.cell(0, 6, "Real-time market data and competitive analysis platform", ln=True)
    pdf.cell(0, 6, "Key Features:", ln=True)
    pdf.cell(0, 5, "  - Market trend analysis", ln=True)
    pdf.cell(0, 5, "  - Competitor tracking and monitoring", ln=True)
    pdf.cell(0, 5, "  - Industry insights and reports", ln=True)
    pdf.cell(0, 5, "  - Customer behavior analytics", ln=True)
    pdf.cell(0, 6, "Ideal For: Marketing teams, business development", ln=True)
    pdf.cell(0, 6, "Value Proposition: 25% improvement in market positioning", ln=True)
    pdf.ln(8)
    
    # Add new page
    pdf.add_page()
    
    # Product 4: Customer Retention System
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Customer Retention System", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, "Monthly Subscription: $399", ln=True)
    pdf.cell(0, 6, "AI-driven customer engagement and retention platform", ln=True)
    pdf.cell(0, 6, "Key Features:", ln=True)
    pdf.cell(0, 5, "  - Churn prediction algorithms", ln=True)
    pdf.cell(0, 5, "  - Personalization engine", ln=True)
    pdf.cell(0, 5, "  - Loyalty program management", ln=True)
    pdf.cell(0, 5, "  - Customer analytics dashboard", ln=True)
    pdf.cell(0, 6, "Benefits: 35% improvement in customer lifetime value", ln=True)
    pdf.cell(0, 6, "Target Users: Customer success teams, retention specialists", ln=True)
    pdf.ln(8)
    
    # Product 5: Enterprise Suite
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Enterprise Suite", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, "Monthly Subscription: $1,999", ln=True)
    pdf.cell(0, 6, "Complete business intelligence and analytics platform", ln=True)
    pdf.cell(0, 6, "Package Includes: All individual products plus premium features", ln=True)
    pdf.cell(0, 6, "Enterprise Features:", ln=True)
    pdf.cell(0, 5, "  - White-label customization options", ln=True)
    pdf.cell(0, 5, "  - Full API access and documentation", ln=True)
    pdf.cell(0, 5, "  - Dedicated account management", ln=True)
    pdf.cell(0, 5, "  - Priority technical support", ln=True)
    pdf.cell(0, 6, "Scalability: Unlimited users and data storage capacity", ln=True)
    pdf.cell(0, 6, "Target: Large enterprises, consulting firms, Fortune 500", ln=True)
    pdf.ln(10)
    
    # Company info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "COMPANY INFORMATION", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, "Wolf AI specializes in AI-powered business intelligence", ln=True)
    pdf.cell(0, 6, "Founded: 2023", ln=True)
    pdf.cell(0, 6, "Headquarters: San Francisco, CA", ln=True)
    pdf.cell(0, 6, "Employees: 150+ professionals", ln=True)
    pdf.cell(0, 6, "Client Base: 500+ companies across 20+ industries", ln=True)
    pdf.cell(0, 6, "Customer Satisfaction: 4.8/5 stars average rating", ln=True)
    
    # Save PDF
    pdf.output("wolf_ai_product_catalog.pdf")
    print("✅ Real PDF created: wolf_ai_product_catalog.pdf")
    return "wolf_ai_product_catalog.pdf"

if __name__ == "__main__":
    pdf_file = create_wolf_ai_catalog_pdf()
    print(f"📄 PDF file ready: {pdf_file}")
    
    # Verify it can be read
    try:
        import PyPDF2
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        print(f"✅ PDF verification successful: {len(text)} characters extracted")
        print(f"📝 Sample content: {text[:100]}...")
    except Exception as e:
        print(f"❌ PDF verification failed: {e}")
