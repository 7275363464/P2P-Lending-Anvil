import anvil.secrets
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
import anvil.media
# from weasyprint import HTML
# from pdf2image import convert_from_bytes
# import io
# from PIL import Image

# all emi receipt
@anvil.server.callable
def create_pdf_from_panel(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.render_form(content_panel)
    
    return pdf

# each emi receipt
@anvil.server.callable
def create_pdf_of_payment_receipt(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4', scale = 0.85).render_form(content_panel)
    
    return pdf

# code to generate pdf of borrower portfolio
@anvil.server.callable
def create_pdf_of_borrower_portfolio(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4').render_form(content_panel)
    
    return pdf

# code to generate pdf of lender portfolio
@anvil.server.callable
def create_pdf_of_lender_portfolio(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4').render_form(content_panel)
    
    return pdf
  

# code to generate pdf of MIS reports
@anvil.server.callable
def create_pdf_of_mis_reports(content_panel):
    # Render the panel to a PDF
    custom_page_size = (28, 35)
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4', scale = 0.85, quality='screen').render_form(content_panel)
    
    return pdf
  
# @anvil.server.callable
# def convert_pdf_to_image(file):
#     pdf_bytes = file.get_bytes()
#     images = convert_from_bytes(pdf_bytes)
    
#     # Convert the first page to PNG
#     img_byte_arr = io.BytesIO()
#     images[0].save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()
    
#     return img_byte_arr