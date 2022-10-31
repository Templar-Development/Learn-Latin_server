from flask import Flask, request
from flask_cors import CORS
import requests
import json
import re

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

@app.route("/ETL", methods=['GET'])
def Whitaker_English_To_Latin():
  args = request.args
  url = f'https://archives.nd.edu/cgi-bin/wordz.pl?english={args.get("word", default="", type=str)}'
  final = format(url, args.get("word", default="", type=str))
  return final

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

app.run(host="0.0.0.0", port="5000")  #run app
