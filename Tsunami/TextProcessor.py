import PyPDF2
from bs4 import BeautifulSoup
from .logger import log


class TextProcessor():
    @staticmethod
    def extract_text_from_paper(paper_path):
        # Read the content of the file
        with open(paper_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Check if the content is HTML
        if "<!DOCTYPE html" in content:
            return TextProcessor.extract_text_from_html(paper_path)
        else:
            # Assuming any non-HTML is PDF
            return TextProcessor.extract_text_from_pdf(paper_path)

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """
        Extracts text from a PDF file.

        Args:
        pdf_path (str): The file path to the PDF from which to extract text.

        Returns:
        str: The extracted text from the PDF.
        """
        # Initialize a text variable to collect all the extracted text
        text = ""

        # Open the PDF file
        with open(pdf_path, "rb") as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Loop through each page in the PDF
            for page in pdf_reader.pages:
                # Extract text from the page and add it to the text variable
                text += page.extract_text() + "\n"  # Adding a newline character after each page's text

        return text

    @staticmethod
    def extract_text_from_html(html_path):
        """
        Extracts text from an HTML file.

        Args:
        html_path (str): The file path to the HTML from which to extract text.

        Returns:
        str: The extracted text from the HTML.
        """
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Extract text using BeautifulSoup
        text = soup.get_text(separator='\n')
        return text