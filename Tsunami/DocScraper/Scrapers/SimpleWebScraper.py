import requests
from urllib.parse import quote
from Tsunami.logger import log
from Tsunami.Utils.basicutils import save_chars_as_file
from Tsunami.DocScraper.DataRequest import DataRequestJob
from Tsunami.TextProcessor import TextProcessor
import os
import tempfile

default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class SimpleWebScraper:
    @staticmethod
    def execute_job(datarequestjob: DataRequestJob, data_download_directory):
        # Extract parameters from the job
        urls = datarequestjob.links  # List of URLs to start with

        for url in urls:
            try:
                log(f"Starting scraping job from URL: {url}", log_type="INFO")

                # Download and clean the page content
                page_content, is_pdf = SimpleWebScraper.download_page_content(url)
                if page_content:
                    # Truncate the URL to a manageable length for the filename
                    max_filename_length = 255
                    sanitized_url = quote(url, safe='')
                    truncated_url = (sanitized_url[:max_filename_length] if len(sanitized_url) > max_filename_length else sanitized_url)

                    if is_pdf:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                            temp_pdf.write(page_content)
                            temp_pdf_path = temp_pdf.name
                        cleaned_page_content = TextProcessor.extract_text_from_paper(temp_pdf_path)
                        os.remove(temp_pdf_path)  # Clean up the temporary file
                    else:
                        cleaned_page_content = TextProcessor.extract_text_from_html_string(page_content)
                    
                    file_path = os.path.join(data_download_directory, f"{truncated_url}.txt")
                    save_chars_as_file(cleaned_page_content, file_path)
                    log(f"Saved scraped page content to {file_path}", log_type="INFO")
            except Exception as e:
                log(f"Error processing URL {url}: {e}", log_type="ERROR")
                continue

    @staticmethod
    def download_page_content(url):
        try:
            response = requests.get(url, headers=default_headers)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            content_type = response.headers.get('Content-Type', '').lower()
            is_pdf = 'application/pdf' in content_type
            return response.content if is_pdf else response.text, is_pdf
        except requests.RequestException as e:
            log(f"Failed to download page content from {url}: {e}", log_type="ERROR")
            return None, False
