import unittest
from src.services.pdf_service import create_pdf

class TestPDFService(unittest.TestCase):

    def test_create_pdf(self):
        # Test the PDF creation functionality
        pdf_content = "This is a test PDF content."
        pdf_file_path = "output/pdf_files/test_output.pdf"
        
        # Call the function to create a PDF
        result = create_pdf(pdf_content, pdf_file_path)
        
        # Check if the PDF file was created successfully
        self.assertTrue(result)
        self.assertTrue(os.path.exists(pdf_file_path))

    def test_create_pdf_empty_content(self):
        # Test the PDF creation with empty content
        pdf_file_path = "output/pdf_files/test_empty_output.pdf"
        
        # Call the function to create a PDF with empty content
        result = create_pdf("", pdf_file_path)
        
        # Check if the PDF file was not created
        self.assertFalse(result)
        self.assertFalse(os.path.exists(pdf_file_path))

if __name__ == '__main__':
    unittest.main()