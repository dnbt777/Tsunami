                              ######################
                              ### Imports/config ###
                              ######################

### Load environment vars ###
from dotenv import load_dotenv
load_dotenv()

### Argument parsing from command line
# Not necessary in your own scripts, but it helps to be able to switch back and forth quickly
import argparse
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument('project_file', type=str, help='Path to the project JSON file')
parser.add_argument('-download', action='store_true', help='Enable downloading of data')
parser.add_argument('-analyze', action='store_true', help='Enable analysis of data')
parser.add_argument('-createrag', action='store_true', help='Generate a RAG db')
parser.add_argument('-analyzerag', action='store_true', help='Analyzing using RAG')
args = parser.parse_args()

PROJECT_FILE = args.project_file
DOWNLOAD = args.download
ANALYZE = args.analyze
RAG = args.createrag
ANALYZE_RAG = args.analyzerag

if not (DOWNLOAD or ANALYZE or RAG or ANALYZE_RAG):
    print("Usage: py ./main.py <any/folders/project_name.json> [-download] [-analyze] [-createrag] [-analyzerag]")
    quit()

### Import AWS boto3 ###
import boto3 # is this needed rn?

### Uncomment the below to turn off excessive AWS debug logging:
#import logging
#for name in logging.Logger.manager.loggerDict.keys():
#   if ('boto' in name) or ('urllib3' in name):
#       logging.getLogger(name).setLevel(logging.WARNING)

### Uncomment to prevent timeout when generating large documents
### should be prevented when streaming but /shrug
#from botocore.config import Config
#config = Config(read_timeout=2000)



                              ######################
                              ### Example script ###
                              ######################

            # DOWNLOAD:  run `py ./main.py <any/folders/project_name.json> -download`
            # ANALYZE:   run `py ./main.py <any/folders/project_name.json> -analyze`
            # BOTH:      run `py ./main.py <any/folders/project_name.json> -download -analyze`

from Tsunami import start_project

# Load configurations
project, downloader, analyzer, rag_generator = start_project(PROJECT_FILE)


# Execute download of files if enabled
# Downloads to ./workspace/[your workspace]/data_downloads/
if DOWNLOAD:
    downloader.execute()


# Execute analysis if enabled
# Stores analyses in ./workspace/[your workspace]/data_analysis/
if ANALYZE:
    analyzer.execute()

# Generate RAG
# Not yet usable for analysis...
if RAG:
    rag_generator.execute()