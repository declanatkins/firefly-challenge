# Firefly Technical Challenge


## Solution Description

I chose to solve this challenge using PySpark and Elasticsearch. The allowed words are parsed and fitered to contain just valid words, and are then loaded into an elasticsearch index. Then, when processing the articles, the words are filtered by querying the elasticsearch index.


## Running the Solution

### Requirements

**For running the solution**
- Docker & Docker Compose

**For running the tests**
- Python 3.8 environment
- In this environment, run `pip install -r testing-requirements.txt`


### Running the solution

On windows with Powershell:
```powershell
.\scripts\run_all.ps1
```

On Mac/Linux:
```bash
./scripts/run_all.sh
```