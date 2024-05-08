import requests
import os
import re
import tarfile
from tqdm import tqdm
import time
from Tsunami.logger import log
from Tsunami.Utils.basicutils import *
from Tsunami.DocScraper.DataRequest import DataRequestJob

class GitHubScraper():
    @staticmethod
    def execute_job(datarequestjob: DataRequestJob, data_download_directory):
        file_types_to_ignore = [] if not hasattr(datarequestjob, 'file_types_to_ignore') else datarequestjob.file_types_to_ignore
        file_types_to_include = [] if not hasattr(datarequestjob, 'file_types_to_include') else datarequestjob.file_types_to_include
        
        if datarequestjob.queries:
            for query in datarequestjob.queries:
                GitHubScraper.scrape_github_search(query, data_download_directory, file_types_to_ignore, file_types_to_include, datarequestjob.document_analysis_limit_per_query)
        if datarequestjob.links:
            for link in datarequestjob.links:
                GitHubScraper.download_repository(link, data_download_directory, file_types_to_ignore, file_types_to_include)

    @staticmethod
    def scrape_github_search(query, download_folder, file_types_to_ignore, file_types_to_include, document_analysis_limit_per_query=5):
        search_url = f"https://api.github.com/search/repositories?q={query}"
        response = requests.get(search_url)
        if response.status_code == 200:
            repositories = response.json()['items'][:document_analysis_limit_per_query]
            for repo in repositories:
                repo_url = repo['html_url']
                GitHubScraper.download_repository(repo_url, download_folder, file_types_to_ignore, file_types_to_include)
        else:
            log(f"Failed to search GitHub: {response.status_code}", log_type="ERROR")

    @staticmethod
    def download_repository(repo_url, download_folder, file_types_to_ignore, file_types_to_include):
        repo_name = repo_url.split('/')[-1]
        repo_api_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/tarball"
        response = requests.get(repo_api_url, stream=True)
        if response.status_code == 200:
            tar_path = os.path.join(download_folder, f"{repo_name}.tar.gz")
            with open(tar_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=1024), desc=f"Downloading {repo_name}"):
                    if chunk:
                        f.write(chunk)
            GitHubScraper.extract_files(tar_path, download_folder, file_types_to_ignore, file_types_to_include)
            os.remove(tar_path)
            log(f"Repository processed: {repo_name}", log_type="INFO")
        else:
            log(f"Failed to download repository: {response.status_code}", log_type="ERROR")

    @staticmethod
    def extract_files(tar_path, extract_to, file_types_to_ignore, file_types_to_include):
        with tarfile.open(tar_path, 'r:gz') as tar:
            if file_types_to_include:
                valid_types = file_types_to_include
            else:
                valid_types = {member.name.split('.')[-1] for member in tar.getmembers()} - file_types_to_ignore

            for member in tar.getmembers():
                if any(member.name.endswith(ft) for ft in valid_types):
                    tar.extract(member, extract_to)

# Example usage
# github_example_job_json = {
#     "source": "github",
#     "queries": [
#         "machine learning",
#         "open source projects",
#     ],
#     "links": [
#         "https://github.com/tensorflow/tensorflow",
#         "https://github.com/numpy/numpy",
#     ],
#     "file_types_to_ignore": [
#         ".png",
#     ],
# }

# # Assuming DataRequestJob is properly defined and can handle GitHub jobs
# data_request_job = DataRequestJob(github_example_job_json)
# GitHubScraper.execute_job(data_request_job, "/path/to/download/directory")


example_file_types_to_include= [
            ".py",
            ".md",
            ".txt",
            ".pyi",
        ]


default_file_types_to_ignore = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".ico",
    ".mp3",
    ".wav",
    ".ogg",
    ".flac",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
    ".mkv",
    ".flv",
    ".3gp",
    ".m4v",
    ".pdf", 
    ".exe",  
    ".bin",  
    ".dll", 
    ".so", 
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".iso",
    ".img",
    ".dmg",  
    ".psd",  
    ".ai",   
    ".eps",  
    ".sketch",
    ".swf",  
    ".fla",  
    ".blend", 
    ".3ds",  
    ".obj",  
    ".fbx",  
    ".stl", 
    ".ply",  
    ".ma",   
    ".mb",   
    ".apk",  
    ".aab",  
    ".ipa", 
]