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

The result obtained was:

```json
*** Top 10 words ***
{
    "the": 44313,
    "and": 20574,
    "that": 9963,
    "for": 9501,
    "its": 7298,
    "you": 6930,
    "with": 6621,
    "will": 4228,
    "this": 4114,
    "but": 4009
}
```

Processing took 61 minutes.