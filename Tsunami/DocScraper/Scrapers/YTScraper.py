import requests
import os
import re
from tqdm import tqdm
import time
from Code.logger import log
from Code.Utils.basicutils import *
from Code.DocScraper.DataRequest import DataRequestJob

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import Playlist
from urllib.parse import urlparse, parse_qs
from Code.logger import log



example_job_json = {
    "source" : "youtube",
    "queries" : [ # TODO
        "cancer treatment 101 tutorial",
        "etc",
    ],
    "links" : [
        "https://www.youtube.com/watch?v=BUE-icVYRFU&ab_channel=YCombinator", # video
        "https://www.youtube.com/watch?v=BUE-icVYRFU&list=PLQ-uHSnFig5M9fW16o2l35jrfdsxGknNB&ab_channel=YCombinator", #playlist of videos
        "etc",
    ],
}


class YTScraper():
    @staticmethod
    def execute_job(datarequestjob : DataRequestJob, data_download_directory):
        #three things: individual links and playlists
        if datarequestjob.queries:
            pass # TODO scrape YT searches
        if datarequestjob.links:
            links = datarequestjob.links
            for link in links:
                youtube_url_type = identify_youtube_url_type(link)
                print(youtube_url_type, link)
                if youtube_url_type == "video":
                    YTScraper.download_video_transcript(link, data_download_directory)
                    pass
                elif youtube_url_type == "playlist":
                    # get each video link
                    video_urls = get_video_urls_from_playlist(link)
                    if datarequestjob.document_analysis_limit_per_playlist:
                        video_urls = video_urls[:datarequestjob.document_analysis_limit_per_playlist]
                    # then get the caption for each video
                    for video_url in video_urls:
                        YTScraper.download_video_transcript(video_url, data_download_directory)
                elif youtube_url_type == "channel":
                    log("YT channel links not currently supported", log_type="ERROR")
                    pass
                else:
                    log(f"Failed to identify youtube link type: {link}", log_type="ERROR")
            


    @staticmethod
    def download_video_transcript(url, download_folder):
        """Get the transcript for a given YouTube video URL."""
        video_id = YTScraper.get_video_id(url)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = youtube_transcript_to_text(transcript)
            file_path = download_folder + f"/{video_id}"
            save_chars_as_file(transcript, file_path)
            return transcript
        except Exception as e:
            log(f"Error retrieving transcript: {e}")
            return None



    @staticmethod
    def get_video_id(url):
        """Extract video ID from URL."""
        parsed_url = urlparse(url)
        video_id = parse_qs(parsed_url.query).get('v')
        if video_id:
            return video_id[0]
        raise ValueError("Invalid YouTube URL")



####
## HELPER FUNCTIONS
####


def identify_youtube_url_type(url):
    # Regular expression for YouTube video URLs
    video_patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',  # Standard YouTube video URL
        r'https?://youtu\.be/[\w-]+',                         # Shortened YouTube video URL
        r'https?://(?:www\.)?youtube\.com/v\?ID=[\w-]+'       # Additional pattern for /v?ID= style URLs
    ]
    
    # Regular expression for YouTube playlist URLs
    playlist_pattern = r'https?://(?:www\.)?youtube\.com/playlist\?list=[\w-]+'
    
    # Check if the URL is a video
    for pattern in video_patterns:
        if re.match(pattern, url):
            return "video"
    
    # Check if the URL is a playlist
    if re.match(playlist_pattern, url):
        return "playlist"
    
    return "neither"



def youtube_transcript_to_text(transcript):
     # Initialize an empty list to store compressed entries
    compressed_entries = []
    
    # Iterate over each dictionary in the input list
    for entry in transcript:
        # Extract text, start, and duration from the dictionary
        text = entry['text']
        start = entry['start']
        duration = entry['duration']
        
        # Create a compressed string for the current entry
        # Format: "start|duration|text"
        compressed_entry = f"{start}|{duration}|{text}"
        
        # Append the compressed entry to the list
        compressed_entries.append(compressed_entry)
    
    # Join all compressed entries with a newline character to form the final compressed string
    compressed_string = "\n".join(compressed_entries)
    
    return "start_time|end_time|text\n" + compressed_string



def get_video_urls_from_playlist(playlist_link):
    # Retrieve URLs of videos from playlist
    playlist = Playlist(playlist_link)
    print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

    urls = []
    for url in playlist:
        urls.append(url)

    return urls