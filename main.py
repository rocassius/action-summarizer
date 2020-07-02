import os
import sys
import urllib.request
from google.cloud import storage

from summarizer import *

# Fetch model
model_file = '/tmp/model.tar'
storage_client = storage.Client()
bucket = storage_client.get_bucket('extraction_bucket_1')
blob = bucket.blob('saved_models/0000360.tar')
blob.download_to_filename(model_file)


def summarize(request):
  request_json = request.get_json(silent=True)
  contains_keys = [k in request_json for k in ["Context", "TaskSentence", "Summary"]]
  if not contains_keys:
    return 'request json missing necessary keys :('

  summarizer  = Summarizer(
    vocab_path = 'vocab.txt',
    model_path = model_file,
    model = TaskModel
  )


  return summarizer.summarize([request_json])