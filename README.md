# Installation

## Requirements
- python 3.x
- Komadu(https://github.com/Data-to-Insight-Center/komadu/)

## How to install
- Install and run Komadu using RabbitMQ
- Install the python requirements
```bash
cd komadu_client
pip install -r requirements.txt
```

# Usage
## Data Extraction from a campaign
```bash
python3.7 komadu_client/main.py --static --workflow_type=<workflow_name> --user=<user_name> --machine=<machine_name> <campaign_dir>
ex:
python3.7 komadu_client/main.py --static --workflow_type="gray-scott" --user=swithana --machine=local ~/codar/campaigns/kTest
```

## Notifications
```bash
python komadu_client/komadu-client.py notify <notification>
ex:
python komadu_client/komadu-client.py notify komadu_client/samples/notifications/gs-output.xml
```

## Querying
```bash
python komadu-client.py query <xml_query>
ex:
python komadu-client.py query samples/singleWorkflowEx/findEntity.xml
```
