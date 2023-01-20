# YouTube API Data Pipeline
<img src="diagram.png"/>

## Prerequisites
* [Google account](https://accounts.google.com/signup)
* [AWS account](https://aws.amazon.com/console/)
* [Python](https://www.python.org/downloads/)
* [VSCode](https://code.visualstudio.com/download)

#### What we're doing

* Getting API key and reading data from YouTube API
* Converting data to CSV and uploading to S3
* Creatin glue job crawls CSV file in S3 bucket and writes it to Redshift DB
* Create Lambda function that runs Glue Job on S3 uploads
* Google Digital Studio creates dashboard with Redshift connection

## Getting YouTube API
* Navigate to the [developer's console](https://console.developers.google.com/) and log in if you haven't already.
* Click 'Create Project' and name your project then click create
* On the APIs & Services console, click 'Enable APIs & Services'
* Search 'YouTube' and click 'YouTube Data API V3' and enable
* On the left hand side, click 'Credentials' then 'Create Credentials'
* Click 'API Key' and save API key

Open VSCode and create a python file and import the following modules:


```ruby
import requests
from googleapiclient.discovery
import pandas as pd
import time
import boto3
import io
```

import channel id (channel you want to track) and api key
how to find channel id

import service name and api version
create api build

This function gets the data of the channel (name, subscribers, view count, video count)

This function gets the video id 

This function gets the video data

converts data to csv

uploads csv file to S3
