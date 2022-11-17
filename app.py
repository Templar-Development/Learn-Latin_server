import json
import re

import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET"])
def home():
  return "<h1>Whitakers Words Thing.</h1>"


@app.route("/LTE", methods=['GET'])
def Whitaker_Latin_To_English():
  args = request.args
  url = f'http://www.archives.nd.edu/cgi-bin/wordz.pl?keyword={args.get("word", default="", type=str)}'
  final = format(url, args.get("word", default="", type=str))
  return final

@app.route("/LTE-T", methods=['GET'])
def Translate_Latin_To_English():
  args = request.args
  url = f'https://languageomega.herokuapp.com/json?lang_one=la&lang_two=en&content={args.get("word", default="", type=str)}'
  response = requests.get(url)
  data = json.loads(response.text)
  return data["TranslatedContent"]

#TODO add a line break inbetween individual definitions
@app.route("/ETL", methods=['GET'])
def Whitaker_English_To_Latin():
  list = []
  args = request.args
  words = args.get("word", default="", type=str).split()
  for i in range(len(words)):
    url = f'https://archives.nd.edu/cgi-bin/wordz.pl?english={words[i]}'
    word = format(url, words[i])
    list.append(word)
  
  return " ".join(list)

@app.route("/ETL-T", methods=['GET'])
def Translate_English_To_Latin():
  args = request.args
  url = f'https://languageomega.herokuapp.com/json?lang_one=en&lang_two=la&content={args.get("word", default="", type=str)}'
  response = requests.get(url)
  data = json.loads(response.text)
  return data["TranslatedContent"]

def format(url, word):
  res = requests.get(url)
  stripped = re.sub('<[^<]+?>', '', res.text)
  remove_title = re.sub('William Whitaker\'s Words', '', stripped)
  final = re.sub(word, '', remove_title, 1)
  return final.strip()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
