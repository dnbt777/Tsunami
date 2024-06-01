# Downloads from pubmedisearch.com - semantic search
gps = {
    "queries" : [
        "cancer in humans",
        "cancer in mice",
        "etc",
        ],
    "document_analysis_limit_per_query" : 10,
}

# Downloads youtube links (TODO add searches/queries)
youtube = {
    "queries" : [ # TODO queries dont work yet
        "cancer treatment 101 tutorial",
        "etc",
    ],
    "links" : [
        "https://youtube.com/v?ID=123012083190a", # video
        "https://playlist for yt", #playlist of videos
        "etc",
    ],
}

# Gets webpages/links from anywhere
{
  "name" : "Karpathy blog",
  "source": "webscraper",
  "links": [
    "http://karpathy.github.io/"
  ],
  "depth" : 2,
  "filter_for_retention": "karpathy\\.github\\.io/\\d+/\\d+/.*",
  "filter_for_avoiding_visiting_site": "^(?!.*karpathy\\.github\\.io).*"
}

# also works for github repos, github queries, and semantic arxiv search
