from src.services.word_service import create_word_document
import unittest
import os

class TestWordService(unittest.TestCase):

    def setUp(self):
        self.output_path = 'output/word_files/test_document.docx'
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_create_word_document(self):
        content = "This is a test document."
        create_word_document(content, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == '__main__':
    unittest.main()