# Analysis Request Examples

This document provides examples of how to structure analysis requests for data that has been collected through various data requests. Each example includes the parameters for the analysis models, the maximum documents per compilation, and the prompts used to guide the analysis.

## Analysis Request Structure

The analysis request JSON object typically contains the following key components:

- `model_analysis_params`: Specifies the models and parameters used for analyzing the documents.
- `prompts`: Contains the instructions or questions that guide the analysis of the documents.

## Example Project (Analysis Request shown at bottom)

```json
{
  "project_config": {
    "workspace": "example_project",
    "cost_tracker": true,
    "ratelimit_delay_seconds": 2,
    "continue_analysis": false
  },

  "data_requests": [
    {
      "name": "Huberman podcast full playlist",
      "source": "youtube",
      "links": [
        "https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW"
      ],
      "document_analysis_limit_per_playlist": 10
    }
  ],

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

### Description of Analysis Request Components

- **Model Analysis Parameters**:
  - `doc_analysis_model`: Specifies the model used for individual document analysis.
  - `recursive_compilation_model`: Specifies the model used for compiling multiple document analyses into fewer documents.
  - `max_docs_per_compilation`: The maximum number of documents that can be compiled together in one iteration.
  - `final_report_model`: Specifies the model used for generating the final report from compiled documents.
  - `max_compilations_per_final_report`: The maximum number of document compilations that will be merged to create the final report.

- **Prompts**:
  - `doc_analysis_prompt`: Provides specific instructions for analyzing the documents. In this example, it asks for relevant quotes related to water intake advice from a podcast.
  - `doc_report_compilation_prompt`: Instructions for how to merge individual document analyses.
  - `final_report_prompt`: Instructions for compiling the final report from the final iteration of merged document analyses.

This example demonstrates how to structure an analysis request to process and analyze data collected from a YouTube playlist, specifically focusing on extracting and compiling information from a series of podcast transcripts. Adjustments can be made based on the specific needs of the analysis task and the nature of the data.

# Important

You only need one analysis_request in the "analysis_requests" field. The field will eventually be renamed to be singular to reflect this.