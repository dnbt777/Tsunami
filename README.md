# Tsunami | Auto Scraping / Cleaning / LLM Analysis
<p align="center">
   <img height="500px" width="500px" src="https://github.com/dnbt777/Tsunami/assets/169108635/d02d3a73-62a4-4cc5-9b0f-4892aa74074c?raw=true"/>
</p>

Tsunami allows you to easily automate scraping data from numerous sources, and then feed it into large language models for analysis.
### Tsunami:
1. Reads your instructions from the project config json - data sources, models to use, prompts, etc.
2. Downloads data from sources
3. Cleans the data, formatting documents into readable versions without extra tokens
4. Sends each doc/file to be analyzed by an LLM (with your specified prompt)
5. Has a model merge each analysis n responses at a time
6. Repeats #4 until it has less than m responses, and then merges the final m responses into a final analysis
A workspace is created in ./workspace/{project_name} containing all doc/data downloads, each response, and the final analysis.
Cost data is output after each response completion, including cumulative cost.


### Terms/Conditions
By using this program you take responsibility for all costs incurred through any/all API usage.

## Quick start
1. git clone https://github.com/dnbt777/Tsunami
2. run `pip install -r requirements.txt`
3. Create a file called ".env" in the below format and fill it out with your keys/region/username
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_USERNAME=
```
4. Run the example script with `python ./example_project.py -download -analyze`


### Currently supported
#### Models:
- Claude (AWS bedrock)

<i>Request a model via DM or by opening an Issue.</i>

#### Data sources:
- Youtube
   - Individual video links
   - Playlist links
- Arxiv semantic search queries
- Pubmed semantic search queries
- Github
   - Repo links
   - Queries for repos



## Usage
Todo



## Documentation/Examples
Coming soon


## Support
Submit an issue, DM me on twitter (https://twitter.com/dnbt777), or DM me on github


#### TODO
Documentation
RAG
Add more models
Save logs
Add more data sources
