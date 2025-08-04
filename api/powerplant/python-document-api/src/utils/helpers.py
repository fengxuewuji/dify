def generate_word_file(content, filename):
    from docx import Document
    doc = Document()
    doc.add_paragraph(content)
    doc.save(filename)

def generate_pdf_file(content, filename):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)

def save_file_to_output_directory(filename, file_type):
    import os
    output_dir = os.path.join('output', f'{file_type}_files')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return os.path.join(output_dir, filename)