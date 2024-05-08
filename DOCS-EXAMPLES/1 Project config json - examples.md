# Create a New Project Guide

This document provides a detailed guide on how to create a new project in the system. It covers setting up the project configuration, defining data requests, and configuring analysis requests.

## Step 1: Define Project Configuration

Start by setting up the basic configuration for your project. This includes specifying the workspace, enabling cost tracking, setting rate limit delays, and deciding whether to continue previous analyses.

### Example Project Configuration

```json
{
  "project_config": {
    "workspace": "example_project",
    "cost_tracker": true,
    "ratelimit_delay_seconds": 2,
    "continue_analysis": false
  }
}
```

- **workspace**: Unique identifier for the project workspace.
- **cost_tracker**: Enables tracking of operational costs.
- **ratelimit_delay_seconds**: Sets a delay between operations to comply with rate limits.
- **continue_analysis**: Determines whether to resume a previously interrupted analysis.

## Step 2: Define Data Requests

Data requests are crucial for specifying what data the project needs to collect. Define each data source, the type of data, and any specific parameters like URLs or query limits.

### Example Data Request for YouTube Data

```json
{
  "name": "Huberman podcast full playlist",
  "source": "youtube",
  "links": [
    "https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW"
  ],
  "document_analysis_limit_per_playlist": 10
}
```

- **name**: Descriptive name for the data request (optional).
- **source**: The data source (e.g., YouTube).
- **links**: Specific URLs to fetch data from.
- **document_analysis_limit_per_playlist**: Limits the number of documents to analyze per playlist.

## Step 3: Define Analysis Requests

Specify how the collected data should be analyzed. This includes choosing models for document analysis, setting up compilation parameters, and writing prompts that guide the analysis process.

### Example Analysis Request Configuration

```json
{
  "analysis_requests": {
    "model_analysis_params": {
      "doc_analysis_model": "haiku",
      "recursive_compilation_model": "haiku",
      "max_docs_per_compilation": 4,
      "final_report_model": "sonnet",
      "max_compilations_per_final_report": 10
    },
    "prompts": {
      "doc_analysis_prompt": "<instructions>Below is a podcast transcript from Andrew Huberman's podcast. Write down relevant quotes from the transcript related to advice on water intake throughout the day.</instructions>",
      "doc_report_compilation_prompt": "<instructions>Merge these analyses docs together, keeping as many detailed points of information as possible.</instructions>",
      "final_report_prompt": "<instructions>Merge these analyses docs together, keeping as many detailed points of information as possible.</instructions>"
    }
  }
}
```

- **model_analysis_params**: Defines the models and parameters for analyzing documents.
- **prompts**: Provides specific instructions for each stage of the analysis.

## Finalizing the Project

Once you have configured the project settings, data requests, and analysis requests, you can initiate the project. Ensure all configurations are correct and aligned with the project goals. The system will then proceed to collect and analyze the data based on the specified parameters.

This guide should help you set up a new project efficiently and ensure that all necessary configurations are in place for successful data collection and analysis.