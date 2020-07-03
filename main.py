import os
import sys
import urllib.request
from google.cloud import storage

from summarizer import *

# classifier dependencies
sys.path.append(os.path.abspath('models'))
import preprocess
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
import fasttext

# load classifier
ft_model = fasttext.load_model("models/best_ft_model.bin")

# Fetch model
model_file = '/tmp/model.tar'
storage_client = storage.Client()
bucket = storage_client.get_bucket('extraction_bucket_1')
blob = bucket.blob('saved_models/0000360.tar')
blob.download_to_filename(model_file)

summarizer  = Summarizer(
    vocab_path = 'vocab.txt',
    model_path = model_file,
    model = TaskModel
  )

def classify_text(request):
  request_json = request.get_json(silent=True)
  email_text = ""
  if request.args and 'message' in request.args:
      email_text = request.args.get('message')
  elif request_json and 'message' in request_json:
      email_text = request_json['message']
  else:
      return f'Something is wrong with request json. :('

  def preprocess_text(text):
    text = sent_tokenize(text)
    out = []
    final_text = ""
    for sentence in text:
        if type(sentence) == str:
            # clean text
            clean = preprocess.clean(sentence)
            # clean info
            clean = preprocess.clean_info(clean)
            out.append(clean)
        else:
            out.append("")
    return out

  sentences = preprocess_text(email_text)

  
  examples = []
  for i in range(len(sentences)):
      prediction = ft_model.predict(sentences[i])
      if "1" in prediction[0][0]:
        sent_dict = {}
        if i > 0:
          sent_dict["Context"] = sentences[i-1]
        else:
          sent_dict["Context"] = ""
        sent_dict["TaskSentence"] = sentences[i] 
        sent_dict["Summary"] = " " 
        
        examples.append(sent_dict)
  res_dict = {"examples": examples}
  # print("RES DICT")
  # print(res_dict)
  return res_dict



def summarize(request_dict):
  summary = summarizer.summarize(request_dict["examples"])
  return summary

def classify_and_summarize(request):
  classified = classify_text(request)
  summarized = summarize(classified)
  return summarized

