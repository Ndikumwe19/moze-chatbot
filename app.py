Skip to content
Search or jump to…
Pull requests
Issues
Codespaces
Marketplace
Explore
 
@Ndikumwe19 
agent87
/
myChatbotApp
Public
forked from renekabagamba/boilerplate-code-chatbot-huzalabs
Fork your own copy of agent87/myChatbotApp
Code
Pull requests
Actions
Projects
Security
Insights
myChatbotApp/app.py /
@agent87
agent87 Trained model
Latest commit 2adf811 yesterday
 History
 1 contributor
95 lines (81 sloc)  3.09 KB

from flask import Flask, render_template, request,jsonify
from flask_ngrok import run_with_ngrok
from flask_cors import CORS
import re
import requests
import json
import detectlanguage
from detectlanguage import simple_detect # import the translator
from flask_sqlalchemy import SQLAlchemy
import datetime
from chat import chatBot


chatBot = chatBot()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:9mcxtgIFPQwi0cKDy8fhEy14YQCLV98M@dpg-cf35u3pgp3jl0q3bmj60-a.oregon-postgres.render.com/chatbot_n9e3"
db = SQLAlchemy(app)
CORS(app)

## Database
class Queries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(1000))
    language = db.Column(db.String(5))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
with app.app_context():
    db.create_all()
    
#from flask import get_response
class translator:
    api_url = "https://translate.googleapis.com/translate_a/single"
    client = "?client=gtx&dt=t"
    dt = "&dt=t"
    #fROM English to Kinyarwanda
    def translate(text : str , target_lang : str, source_lang : str):
        sl = f"&sl={source_lang}"
        tl = f"&tl={target_lang}"
        r = requests.get(translator.api_url+ translator.client + translator.dt + str(sl) + str(tl) + "&q=" + str(text))
        return json.loads(r.text)[0][0][0]

# use this link to get your api key https://detectlanguage.com/
detectlanguage.configuration.api_key = "13e26484ba8a0a3d865573c4868de0a0"
detectlanguage.configuration.secure = True

def process_question(text : str):
  source_lang = simple_detect(text)
  resp = translator.translate(text=text, target_lang='en', source_lang=source_lang)
  return resp, source_lang

def process_answer(text : str, source_lang):
  resp = translator.translate(text=text, target_lang=source_lang, source_lang='en')
  return resp

def preprocessing(text):
    text = text.lower()
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    html_pattern = re.compile('<.*?>')
    text = url_pattern.sub(r'', text)
    text = html_pattern.sub(r'', text)
    text = re.sub(r"[^\w\d'\s]+", ' ', text)
    return text
Q = []
R = []

def process(QUESTION: str):
    Q.append(QUESTION)
    USER_QUERY, SL = process_question(QUESTION) #Translate the original question into english and store the source lang
    RESPONSE = chatBot.get_response(USER_QUERY) #Asking the chatbot question
    ORIGINAL_RESPONSE = process_answer(RESPONSE, SL)
    R.append(ORIGINAL_RESPONSE)
    return ORIGINAL_RESPONSE, SL

@app.route("/",  methods=["GET"])
def index_get():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    text = request.get_json().get("message")
    #check if text is valid (I let it for you)
    response, sl = process(text)
    # we jsonify our response
    message = {"answer":response}
    query = Queries(question=text, answer=response, language=sl)
    db.session.add(query)
    db.session.commit()
    return jsonify(message)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
myChatbotApp/app.py at main · agent87/myChatbotApp
