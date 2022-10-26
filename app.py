
from flask import Flask,render_template,request,url_for
from ibm_watson import LanguageTranslatorV3,SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

def sttfunction(audio):
    #with open(audio, mode='rb') as f:
    res = stt.recognize(audio=audio, content_type='audio/mp3', model='en-AU_NarrowbandModel').get_result()
    return res['results'][0]['alternatives'][0]['transcript']

def ident(text):
    language = lt.identify(text).get_result()
    return language

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/audio.html")
def audio():
    return render_template("audio.html")

@app.route("/identifier.html")
def identifier():
    return render_template("identifier.html")

@app.route("/micro.html")
def micro():
    return render_template("micro.html")


#API Key and Url variables :
ltapikey = '6L5MwgdUkr8-_5jsjlJdnkEaQ818f2X9lAM5Jg0V1P2B'
lturl = 'https://api.au-syd.language-translator.watson.cloud.ibm.com/instances/f36bdb17-2608-4cea-938c-913951f165a5'

sttapikey = '8M4rD93kMtz9mGOhLts40qRKDVp4DFJRKVaTktEooEDz'
stturl = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/695dfb31-09dd-4ee7-b962-8a7fc2805466'
    
#Authentification grâce à : Apikey et api url
ltauthenticator = IAMAuthenticator(ltapikey)
lt = LanguageTranslatorV3(version='2020-07-01', authenticator=ltauthenticator)
lt.set_service_url(lturl)

sttauthenticator = IAMAuthenticator(sttapikey)
stt = SpeechToTextV1(authenticator=sttauthenticator)
stt.set_service_url(stturl)

#Fonction de traduction utilisant la méthode translate elle retourne la traduction, la nombre de mots/caractères
def translate(t,m):

    translation = lt.translate(text=t, model_id=m).get_result()
    return translation


@app.route("/result",methods=["POST"])
def result():
    text = request.form['text']
    model= request.form['model']
    result=translate(text,model)
    return render_template("home.html",translation=result['translations'][0]['translation'],wordcount=result['word_count'],character=result['character_count'])


@app.route('/result2',methods=["POST"])
def result2():
    file = request.files['file'].read()
    model = request.form['model']
    text=sttfunction(file)
    voicetext=translate(text,model)
    return render_template("audio.html",translation=voicetext['translations'][0]['translation'],wordcount=voicetext['word_count'],character=voicetext['character_count'])


@app.route('/result3',methods=["POST"])
def result3():
    text = request.form['text']
    t=ident(text)
    return render_template("identifier.html",model=t['languages'][0]['language'],confidence=t['languages'][0]['confidence'])

@app.route("/result4",methods=["POST"])
def result4():
    text = request.form['speechToText']
    model= request.form['model']
    result4=translate(text,model)
    return render_template("micro.html",translation=result4['translations'][0]['translation'],wordcount=result4['word_count'],character=result4['character_count'])

if __name__ == "__main__":
    app.run(debug=True)





    