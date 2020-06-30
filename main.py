import os
import sys
import urllib.request

# Fetch Model
model_url = 'https://storage.cloud.google.com/extraction_bucket_1/saved_models/0000360.tar'
model_file, headers = urllib.request.urlretrieve(model_url, filename='/tmp/model.tar')

def summarize(request):
  request_json = request.get_json(silent=True)
  contains_keys = [k in request_json for k in ["Context", "TaskSentence", "Summary"]]
  if not contains_keys:
    return 'request json missing necessary keys :('

  return model_file