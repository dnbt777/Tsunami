# Writing a Simple Script Guide

This document provides a detailed guide on how to write a simple Python script to execute tasks such as downloading and analyzing data. The script will handle command-line arguments to toggle between downloading, analyzing, or doing both.

## Step 1: Setup and Configuration

Start by setting up your Python script with the necessary imports and configurations.

### Basic Imports and Environment Setup

```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

import argparse  # Import argparse for command-line argument parsing
```

### Command-Line Argument Parsing

Set up argparse to handle command-line options for downloading and analyzing data.

```python
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument('-download', action='store_true', help='Enable downloading of data')
parser.add_argument('-analyze', action='store_true', help='Enable analysis of data')
args = parser.parse_args()

DOWNLOAD = args.download
ANALYZE = args.analyze

if not (DOWNLOAD or ANALYZE):
    print("Usage: ./example_project.py [-download] [-analyze]")
    quit()
```

- **-download**: Flag to enable data downloading.
- **-analyze**: Flag to enable data analysis.
- **Usage message**: Printed if no flags are provided.

### Optional AWS Configuration

If your script interacts with AWS services, you might need to import and configure the AWS SDK for Python (boto3).

```python
import boto3

# Optional: Configure logging to reduce verbosity
import logging
for name in logging.Logger.manager.loggerDict.keys():
    if ('boto' in name) or ('urllib3' in name):
        logging.getLogger(name).setLevel(logging.WARNING)
```

## Step 2: Define Main Functionality

Define the main functionality of your script, which includes initializing project components and executing tasks based on command-line arguments.

### Initialize Project Components

Use a function to load project configurations and initialize components like the downloader and analyzer.

```python
from Tsunami import start_project
project, downloader, analyzer = start_project('example_project.json')
```

### Execute Download

Check if the download flag is set and execute the download process.

```python
if DOWNLOAD:
    downloader.execute()  # Execute the download process
```

### Execute Analysis

Check if the analyze flag is set and execute the analysis process.

```python
if ANALYZE:
    analyzer.execute()  # Execute the analysis process
```

## Step 3: Running the Script

To run the script, use the following commands based on what you need to do:

- **Download Only**: `./example_project.py -download`
- **Analyze Only**: `./example_project.py -analyze`
- **Both Download and Analyze**: `./example_project.py -download -analyze`

This guide provides a basic framework for writing a Python script that handles command-line arguments to perform tasks like downloading and analyzing data. Adjust the script based on the specific requirements and functionalities of your project.