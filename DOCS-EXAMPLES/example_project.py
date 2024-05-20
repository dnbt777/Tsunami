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
parser.add_argument('-download', action='store_true', help='Enable downloading of data')
parser.add_argument('-analyze', action='store_true', help='Enable analysis of data')
args = parser.parse_args()

DOWNLOAD = args.download
ANALYZE = args.analyze

if not (DOWNLOAD or ANALYZE):
    print("Usage: ./example_project.py [-download] [-analyze]")
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

                # DOWNLOAD:  run `./example_project.py -download`
                # ANALYZE:   run `./example_project.py -analyze`
                # BOTH:      run `./example_project.py -download -analyze`

from Tsunami import start_project

# Load configurations
project, downloader, analyzer = start_project('example_project.json')


# Execute download of files if enabled
# Downloads to ./workspace/[your workspace]/data_downloads/
if DOWNLOAD:
    downloader.execute()


# Execute analysis if enabled
# Stores analyses in ./workspace/[your workspace]/data_analysis/
if ANALYZE:
    analyzer.execute()
