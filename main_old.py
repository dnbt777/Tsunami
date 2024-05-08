import logging

from dotenv import load_dotenv
import time
#from Code.EggFinder import EggFinder
from Code.logger import log
#from Code.TestSuite import TestSuite
from Code.DocScraper.DocScraperManager import DocScraperManager
from Code.DocScraper.DataRequest import DataRequestJob, DataRequestJobs
from Code.DataAnalysis.DataAnalysisManager import DataAnalysisManager
from Code.DataAnalysis.DataAnalysisJob import DataAnalysisJob
from Code.ProjectConfig import ProjectConfig
from Code.Metrics.CostTracker import CostTracker

# Load environment vars
load_dotenv()

# Turn off excessive AWS debug logging
import boto3
for name in logging.Logger.manager.loggerDict.keys():
    if ('boto' in name) or ('urllib3' in name):
        logging.getLogger(name).setLevel(logging.WARNING)

# Prevent timeout when generating large documents
from botocore.config import Config
config = Config(read_timeout=2000)



DOWNLOAD=True
ANALYZE=True
CONTINUE_ANALYSIS=False # use if analysis broke halfway - need analyze=True to be on


def main():
    # Set up project configuration
    cost_tracker = CostTracker()

    # Each project has a workspace
    project_config_dict = {
        "workspace" : "2_twitter_howmuchwater_huberman",
        "cost_tracker" : cost_tracker,
        "ratelimit_delay_seconds" : 2,
        "continue_analysis" : CONTINUE_ANALYSIS
    }
    project_config_obj = ProjectConfig(**project_config_dict)


    # Example data request, sent from the front end (in JSON or something)
    gps_datarequest_json =  {
            "source" : "gps",
            "queries" : [
                "unconscious and goals",
                "results of utilizing the unconscious brain",
                "the unconscious brain",
                ],
            "document_analysis_limit_per_query" : 2,
    }
    youtube_playlist_datarequest_json = {
        "source" : "youtube",
        "links" : [
            "https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW", # Huberman podcast
        ],
        "document_analysis_limit_per_playlist" : 10,
    }
    youtube_datarequest_json = {
            "source" : "youtube",
            "queries" : [ # NOT YET IMPLEMENTED
                "cancer treatment 101 tutorial",
                #"etc",
            ],
            "links" : [
                "https://www.youtube.com/watch?v=zHECSAdJjTQ&t=495&ab_channel=ColinGalen", # video
                #"https://playlist for yt", #playlist of videos
                #"channel - get top videos from channel",
            ],
        }
    arxiv_datarequest_json = {
        "source" : "arxiv",
        "queries" : [
            "compression is intelligence",
        ],
        "document_analysis_limit_per_query" : 2,
    }
    webcrawler_dararequest_json = {
        "source" : "webcrawler",
        "links" : [
            "https://www.citadelsecurities.com/careers/open-opportunities/positions-for-professionals/",
        ],
        "depth" : 2,
        "filter_for_retention" : (lambda url: "https://www.citadelsecurities.com/careers/" in url),
        "filter_for_avoiding_visiting_site" : (lambda url: not ("careers" in url)),
    }
    compression_is_intelligence_json = {
        "source" : "arxiv",
        "queries" : [
            "compression is intelligence",
        ],
        "document_analysis_limit_per_query" : 20,
    }
    github_example_job_json = {
        "source": "github",
        "queries": [
            #"machine learning",
            #"open source projects",
        ],
        "links" : [
            "https://github.com/numpy/numpy",
        ],
        "file_types_to_include" : [
            ".py",
            ".md",
            ".txt",
            ".pyi",
        ],
        "document_analysis_limit_per_query" : 2,
    }
    huberman_gains_yt = {
        "source" : "youtube",
        "links" : [
            "https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW",
        ],
        "document_analysis_limit_per_playlist" : 300,
    }
    datarequestjobs_list_json = [
        # gps_datarequest_json,
        # youtube_datarequest_json,
        # arxiv_datarequest_json,
        # youtube_playlist_datarequest_json,
        # webcrawler_dararequest_json,
        # compression_is_intelligence_json,
        #github_example_job_json,
        huberman_gains_yt,
    ]
    #datarequestjobs_list_json.append(gps_datarequest_json)
    print(datarequestjobs_list_json)


    if DOWNLOAD:
        # Create DataRequestJobs object
        datarequestjobs = DataRequestJobs(datarequestjobs_list_json) # should NOT hold workspace info

        # Load up a docscraper with workspace config vars, then execute jobs
        docscraper = DocScraperManager(project_config_obj) # should hold workspace info
        docscraper.execute_jobs(datarequestjobs) # Docs are now downloaded into workspaces/[workspace]/downloads/{scraper}

    if ANALYZE:
        # for now just analyze everything in /downloads/...
        # at the moment, no of duments to analyze will be set at the download stage
        compression_is_intelligence_prompt = """I want to understand the concept of "compression is intelligence" better. Don't give me info about specific machine learning techniques or named frameworks around understanding compression"""
        compression_is_intelligence_prompt = """<instructions>
                    An expert wants to find useful insights related to their prompt. Their message is <expert_prompt>{user_prompt}</expert_prompt> Analyze the provided document.
                    EXPLICIT INSIGHTS SECTION: Find numerous interesting and useful insights related to the expert's prompt, as well as their implications.
                    IMPLICIT INSIGHTS SECTION: Useful information may be several logical conclusions ahead, and may not be explicitly stated in the document. In <brainstorming></brainstorming> XML tags, provide a lengthy brainstorming session to generate insights, thinking step by step for numerous steps. Then write the implicit insights in the implicit insights section, similar to the explicit insights section. The brainstorming section is your room to think out loud, and no content in it will be saved, so put the implicit insights outside of this section along with the rationales that lead to them.
                    HYPOTHESES SECTION: Then, generate logical hypotheses about useful possibilities and interesting logical conclusions of this information.
                </instructions>"""
        no_prompt = """[no prompt provided, continue with default instructions]"""
        huberman_will_prompt = """<instructions>Below is a podcast transcript from Andrew Huberman's podcast. Write down all information related to answering the following question: What is the optimal way (health wise) to spend the last 4 hours of your day before you sleep?</instructions>""" # + <transcript>
        huberman_twitter_prompt = """<instructions>Below is a podcast transcript from Andrew Huberman's podcast. Write down all information from the transcript (starting with the relevant quote for each piece of info) related to advice on water intake throughout the day. Only write down information gathered from the podcast, from which a quote can be stated. </instructions>""" # + <transcript>
        github_repo_prompt = "<instructions>Below is the contents of a file from the numpy github repo. 1) Tell me what non-obvious useful information/insights you can gather about the usage of numpy from this file, that an average numpy user wouldn't know. 2) give creative examples of how the nuanced information tidbits you gathered from the file could be used to better leverage the repo's software</instructions>"
        

        doc_analysis_prompt = huberman_twitter_prompt

        analysisrequestjobs_json = { 
            "model_analysis_params" : {
                # Model to analyze each doc -> DocAnalysis
                "doc_analysis_model"            : "haiku",
                # "doc_chunk_size"                : 10_000,  # breaks up large documents into several chunks

                # Model to recursively stitch together DocAnalysis objects -> [DocAnalysis, DocAnalysis ...] -> DocAnalysis
                # Do this until there are less than {max_compilations_per_final_report} DocAnalysis objects left
                "recursive_compilation_model"   : "haiku",
                "max_docs_per_compilation"      : 4, # only stitches max of 3 together at once

                # Model to generate final report out of DocAnalysis objects
                "final_report_model"            : "sonnet",
                "max_compilations_per_final_report" : 10, # => f(10 doc analyses) -> final report
            },
            "prompts" : {
                "doc_analysis_prompt" : doc_analysis_prompt, # primary user input
                "doc_report_compilation_prompt" : """<instructions>
                    Merge these analyses docs together, keeping as many of the insights and hypothesis as possible. Keep a similar format.
                </instructions>""", # recommended to not make this user input
                "final_report_prompt" : """<instructions>
                    Merge these analyses docs together, keeping as many of the insights and hypothesis as possible. Keep a similar format.
                </instructions>""" # recommended to not make this user input
            },
            "excluded_directories" : [
                "/spotify", # example
            ]  #directories in /downloads/* to exclude from analysis
        }


        data_analysis_manager = DataAnalysisManager(project_config_obj)
        data_analysis_job = DataAnalysisJob(analysisrequestjobs_json)

        data_analysis_manager.execute_job(data_analysis_job) # Analyses are now downloaded into workspaces/[workspace]/analysis/{analysis_prompt_id}/{(doc_analyses, doc_compilations, final_report)}

        #project_config_obj.cost_tracker.show_cost_data()




if __name__ == "__main__":
    main()