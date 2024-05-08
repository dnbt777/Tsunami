import requests
import os
from tqdm import tqdm
import time
from Code.logger import log
from Code.Utils.basicutils import *
from Code.DocScraper.DataRequest import DataRequestJob
from Code.TextProcessor import TextProcessor


class SemanticArxivScraper():
    @staticmethod
    def execute_job(datarequestjob : DataRequestJob, data_download_directory):
        for query in datarequestjob.queries:
            paper_pdf_links = SemanticArxivScraper.fetch_articles(query) # Get article info
            SemanticArxivScraper.download_pdf_of_papers_from_links(
                paper_pdf_links,
                download_folder=data_download_directory,
                document_downloads_per_query=datarequestjob.document_analysis_limit_per_query
            ) # Download each article


    @staticmethod
    def fetch_articles(query):
        url = "https://us-west1-semanticxplorer.cloudfunctions.net/semantic-xplorer-db?query=" + query.replace(' ', '+')
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,es;q=0.8,fr;q=0.7,it;q=0.6,da;q=0.5",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site"
        }
        params = {
            "query": query
        }
        response = requests.get(url) #, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


    @staticmethod
    def download_pdf_of_papers_from_links(paper_metadata_list, download_folder, document_downloads_per_query=1e7):
        log(f"Downloading articles to {download_folder}/...")
        for index, paper_metadata in tqdm(list(enumerate(paper_metadata_list))[:document_downloads_per_query]): # converting to list allows tqdm to show full amnt of docs
            time.sleep(2) # sleeps 2 seconds to not spam server
            # Download pdf
            paper_pdf_link = f"https://arxiv.org/pdf/{paper_metadata['id']}"
            cleaned_filename = clean_string_for_file_system(paper_metadata["metadata"]['title']) + '.pdf'
            paper_pdf_download_path = f"{download_folder}/{cleaned_filename}"
            download_pdf(paper_pdf_link, download_folder, cleaned_filename)
            # Get content from the pdf
            cleaned_paper_content = TextProcessor.extract_text_from_paper(paper_pdf_download_path)
            file_path = f'{download_folder}/{cleaned_filename}.txt'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_paper_content)
            # Delete the pdf so it doesnt get analyzed
            print(paper_pdf_download_path)
            os.remove(paper_pdf_download_path)


def download_pdf(paper_pdf_link, download_folder, filename):
    
    # Create the directory './test' if it does not exist
    os.makedirs(download_folder, exist_ok=True)
    
    # Full path to save the file
    save_path = download_folder + '/' + filename
    
    # Send a GET request to the url
    response = requests.get(paper_pdf_link)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary write mode and save the content
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"File saved as {save_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    return save_path