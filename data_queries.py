
pps_pubmed = {
    "query_lists" : [[
        "cancer in men",
        "cancer in women",
        "etc"
    ]],
    "document_analysis_limit_per_query" : 10,
}

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
    "queries" : [ # TODO
        "cancer treatment 101 tutorial",
        "etc",
    ],
    "links" : [
        "https://youtube.com/v?ID=123012083190a", # video
        "https://playlist for yt", #playlist of videos
        "etc",
    ],
}

# Downloads spotify transcripts - uses semantic search for queries
spotify = {
    "queries" : [
        "cancer treatment expert",
        "cancer expert podcast",
        "etc",
    ],
    "links" : [
        "add links to podcasts here"
    ],
    "document_analysis_limit_per_query" : 10,
}

# Googles top x pages and gets them, per query
google = {
    "queries" : [
        "cancer blog -astrology -recipes",
        "cancer expert posts site:cancerexperts.com",
        "etc",
        ],
    "document_analysis_limit_per_query" : 10,
}

# Gets webpages/links from anywhere
webpages = {
    "links" : [
        "https://reddit.com/r/cancer/123908123",
        "https://pubmed.org/102392812089",
        "etc"
    ],
    "special_links" : [
        "https://blog.cancer.com/page/{n}", # write some sort of parsing function
    ],
    "document_analysis_limit_per_query" : 10, # applies to special links - picks first 10
}