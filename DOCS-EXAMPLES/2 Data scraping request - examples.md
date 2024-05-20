# Data Request Examples

This document provides examples of different types of data requests that can be made using the system. Each example includes the source of the data, the specific parameters used for the request, and the intended use of the data.

## GPS Data Request

```json
{
    "source": "gps",
    "queries": [
        "unconscious and goals",
        "results of utilizing the unconscious brain",
        "the unconscious brain"
    ],
    "document_analysis_limit_per_query": 2
}
```
- **Description**: Requests data from a GPS source based on specified queries.
- **Limit**: Limits the number of documents analyzed per query to 2.

## YouTube Playlist Data Request

```json
{
    "source": "youtube",
    "links": [
        "https://www.youtube.com/playlist?list=PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW"
    ],
    "document_analysis_limit_per_playlist": 10
}
```
- **Description**: Fetches data from a specified YouTube playlist.
- **Limit**: Analyzes up to 10 documents from the playlist.

## YouTube Data Request

```json
{
    "source": "youtube",
    "queries": [
        "cancer treatment 101 tutorial"
    ],
    "links": [
        "https://www.youtube.com/watch?v=zHECSAdJjTQ&t=495&ab_channel=ColinGalen"
    ]
}
```
- **Description**: Requests data from YouTube based on search queries and specific video links.

## ArXiv Data Request

```json
{
    "source": "arxiv",
    "queries": [
        "compression is intelligence"
    ],
    "document_analysis_limit_per_query": 2
}
```
- **Description**: Fetches documents from ArXiv based on specified queries.
- **Limit**: Limits the number of documents analyzed per query to 2.

## "DepthCrawler" Web Crawler Data Request (incomplete)

```json
{
    "source": "webcrawler",
    "links": [
        "https://www.example.com/careers/open-opportunities/positions-for-professionals/"
    ],
    "depth": 2,
    "filter_for_retention": "lambda url: 'https://www.example.com/careers/' in url",
    "filter_for_avoiding_visiting_site": "lambda url: not ('careers' in url)"
}
```
- **Description**: Uses a web crawler to fetch data from specified links with depth control and URL filtering.

## GitHub Data Request

```json
{
    "source": "github",
    "links": [
        "https://github.com/numpy/numpy"
    ],
	"query": [
		"transformer with KAN feed forward"
	]
    "file_types_to_include": [
        ".py",
        ".md",
        ".txt",
        ".pyi"
    ],
    "document_analysis_limit_per_query": 2
}
```
- **Description**: Fetches data from GitHub repositories, specifically targeting files of certain types.

Each of these examples demonstrates how to structure a data request for different sources using the system. The parameters can be adjusted based on the specific needs of the data retrieval or analysis task.
