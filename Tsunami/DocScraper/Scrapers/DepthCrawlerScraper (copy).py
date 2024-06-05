import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote, urljoin
import re
from Tsunami.logger import log
from Tsunami.Utils.basicutils import save_chars_as_file
from Tsunami.DocScraper.DataRequest import DataRequestJob
from Tsunami.TextProcessor import TextProcessor
import time
import os

default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class DepthCrawlerScraper:
    @staticmethod
    def execute_job(datarequestjob: DataRequestJob, data_download_directory):
        # Extract parameters from the job
        url = datarequestjob.links[0]  # Assuming the first link is the starting URL
        depth = datarequestjob.depth
        filter_for_retention = datarequestjob.filter_for_retention
        filter_for_avoiding_visiting_site = datarequestjob.filter_for_avoiding_visiting_site
        scraping_delay = datarequestjob.ratelimit_delay_seconds

        log(f"Starting scraping job from URL: {url} with depth: {depth}", log_type="INFO")

        # Start scraping
        scraped_urls = DepthCrawlerScraper.scrape(url, depth, filter_for_retention,
                                                  filter_for_avoiding_visiting_site=filter_for_avoiding_visiting_site,
                                                  scraping_delay=scraping_delay)
        log(f"Scraping complete. Total URLs scraped: {len(scraped_urls)}", log_type="INFO")

        # Save scraped page contents to files
        for scraped_url in scraped_urls:
            page_content = DepthCrawlerScraper.download_page_content(scraped_url)
            if page_content:
                sanitized_url = quote(scraped_url, safe='')  # Sanitize URL to be used as a filename
                cleaned_page_content = TextProcessor.extract_text_from_html_string(page_content)
                file_path = os.path.join(data_download_directory, f"{sanitized_url}.txt")
                save_chars_as_file(cleaned_page_content, file_path)
                log(f"Saved scraped page content to {file_path}", log_type="INFO")

    @staticmethod
    def scrape(url, depth, filter_for_retention, filter_for_avoiding_visiting_site=None, scraping_delay=1):
        urls = []
        urls_to_scrape = [url]
        log(f"Initiating scrape with base URL: {url}", log_type="INFO")

        for current_depth in range(depth):
            urls_to_scrape_next_depth = []
            log(f"Scraping depth {current_depth + 1}/{depth}", log_type="INFO")

            for current_url in urls_to_scrape:
                if filter_for_avoiding_visiting_site and re.search(filter_for_avoiding_visiting_site, current_url):
                    log(f"Skipping URL due to filter: {current_url}", log_type="LOG")
                    continue

                page_content = DepthCrawlerScraper.download_page_content(current_url)
                if page_content:
                    scraped_urls = DepthCrawlerScraper.get_urls_from_html(page_content, current_url)
                    time.sleep(scraping_delay)
                    log(f"Found {len(scraped_urls)} URLs from {current_url}", log_type="LOG")

                    for new_url in scraped_urls:
                        if new_url not in urls and new_url not in urls_to_scrape_next_depth:
                            if re.search(filter_for_retention, new_url):
                                urls_to_scrape_next_depth.append(new_url)

            urls.extend(urls_to_scrape)
            urls_to_scrape = urls_to_scrape_next_depth

        retained_urls = [url for url in urls if re.search(filter_for_retention, url)]
        log(f"Retained {len(retained_urls)} URLs after filtering", log_type="INFO")
        return retained_urls

    @staticmethod
    def download_page_content(url):
        try:
            response = requests.get(url, headers=default_headers)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            log(f"Failed to download page content from {url}: {e}", log_type="ERROR")
            return None

    @staticmethod
    def get_urls_from_html(page_content, base_url):
        try:
            soup = BeautifulSoup(page_content, 'html.parser')
            links = [urljoin(base_url, link.get('href')) for link in soup.find_all('a', href=True)]
            log(f"Downloaded and parsed {len(links)} links from page content", log_type="LOG")
            log(links)
            return links
        except Exception as e:
            log(f"DepthCrawler: Failed to get urls from page content: {e}", log_type="ERROR")
            return []