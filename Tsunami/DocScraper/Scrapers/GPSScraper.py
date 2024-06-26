import requests
import os
from tqdm import tqdm
import time
from Tsunami.logger import log
from Tsunami.Utils.basicutils import *
from Tsunami.DocScraper.DataRequest import DataRequestJob


class GPSScraper():
    @staticmethod
    def execute_job(datarequestjob : DataRequestJob, data_download_directory):
        for query in datarequestjob.queries:
            articles = GPSScraper.gps_fetch_articles(query) # Get article info
            GPSScraper.gps_download_html_of_papers(
                articles,
                download_folder=data_download_directory,
                document_downloads_per_query=datarequestjob.document_analysis_limit_per_query
            ) # Download each article


    @staticmethod
    def gps_fetch_articles(query):
        url = "https://www.pubmedisearch.com/api/fetch_articles"
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,es;q=0.8,fr;q=0.7,it;q=0.6,da;q=0.5",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        body = {
            "query": query,
            "userId": "949b208c-e2c7-4173-a12c-071be0be2d22"
        }
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


    @staticmethod
    def gps_download_html_of_papers(articles, download_folder, document_downloads_per_query=1e7):
        log(f"Downloading articles to {download_folder}/...")
        for index, article in tqdm(list(enumerate(articles))[:document_downloads_per_query]): # converting to list allows tqdm to show full amnt of docs
            time.sleep(2) # sleeps 2 seconds to not spam server
            response = requests.get(article['url'])
            if response.status_code == 200:
                cleaned_filename = clean_string_for_file_system(article["title"])
                cleaned_paper_content = clean_html_string(response.text)
                file_path = f'{download_folder}/gps_{cleaned_filename}.html'
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_paper_content)
            else:
                log(f"Failed to download {article['title']}")
