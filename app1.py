from pyexpat import model
from flask import Flask,render_template,request
import pickle
from ibm_watson import SpeechToTextV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from numpy import character






app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home1.html")

def translate(t,m):
    ltapikey = '6L5MwgdUkr8-_5jsjlJdnkEaQ818f2X9lAM5Jg0V1P2B'
    lturl = 'https://api.au-syd.language-translator.watson.cloud.ibm.com/instances/f36bdb17-2608-4cea-938c-913951f165a5'
    

    ltauthenticator = IAMAuthenticator(ltapikey)
    lt = LanguageTranslatorV3(version='2020-07-01', authenticator=ltauthenticator)
    lt.set_service_url(lturl)

    translation = lt.translate(text=t, model_id=m).get_result()
    tr=translation['translations'][0]['translation']
    wordcount=translation['word_count']
    character=translation['character_count']

    return tr,wordcount,character

@app.route("/result",methods=["POST"])
def result():
    text = request.form['text']
    model= request.form['model']
    result=translate(text,model)
    return render_template("result.html",result=result)

if __name__ == "__main__":
    app.run(debug=True)