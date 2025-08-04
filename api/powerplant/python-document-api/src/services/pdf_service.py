from fpdf import FPDF

class PDFService:
    def __init__(self):
        self.pdf = FPDF()

    def create_pdf(self, title, content, output_path):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(0, 10, title, ln=True, align='C')
        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(0, 10, content)
        self.pdf.output(output_path)

def generate_pdf(title, content, output_file):
    pdf_service = PDFService()
    pdf_service.create_pdf(title, content, output_file)