import os
import sys
import urllib.request
from summarizer import *

# Fetch Model
model_url = 'https://storage.cloud.google.com/extraction_bucket_1/saved_models/0000360.tar'
model_file, headers = urllib.request.urlretrieve(model_url, filename='/tmp/model.tar')
keys = ["Context", "TaskSentence", "Summary"]


def lambda_handler(event, context):
    
    # Check for missing keys
    if not all([k in event.keys() for k in keys]):
        return {
            'statusCode': 200,
            'body': 'missing data...something is wrong'
        }
    
