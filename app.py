from flask import Flask,render_template,request
from transformers import T5ForConditionalGeneration, T5Tokenizer
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi as ytt
from flask import Flask, render_template, request
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer
import torch
from flask_mysqldb import MySQL
from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response)
import os
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
 
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
        
mysql = MySQL()
app = Flask(__name__,static_folder='static')
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'chat'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app = Flask(__name__)

# Load the pretrained model
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')

# initialize the model architecture and weights
model_t = T5ForConditionalGeneration.from_pretrained("t5-small")
# initialize the model tokenizer
tokenizer_t = T5Tokenizer.from_pretrained("t5-small")
# define your resource endpoints
history = []

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('Home.html')


#extracts id from url
def extract_video_id(url:str):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    history=url
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail?
    return None
#text summarizer
def summarizer(script):
    # encode the text into tensor of integers using the appropriate tokenizer
    input_ids = tokenizer_t("summarize: " + script, return_tensors="pt", max_length=2048, truncation=True).input_ids
    # generate the summarization output
    outputs = model_t.generate(
        input_ids, 
        max_length=2000, 
        min_length=500, 
        length_penalty=2.0, 
        num_beams=6, 
        early_stopping=True)

    summary_text = tokenizer_t.decode(outputs[0])
    return(summary_text)

def write_text(text):
    with open("text.txt", "w") as file:
        file.write('\n' + text)
        
@app.route('/summarize',methods=['GET','POST'])
def video_transcript():
    if request.method == 'POST':
        url = request.form['youtube_url']
        video_id = extract_video_id(url)
        data = ytt.get_transcript(video_id,languages=['de', 'en'])
        print("data--------",data)
        
        scripts = []
        for text in data:
            for key,value in text.items():
                if(key=='text'):
                    scripts.append(value)
        transcript = " ".join(scripts)
        print("transcript---------------",transcript)
        summary = summarizer(transcript)
        summary = summary.replace("</s>","")
        summary = summary.replace("<pad>","")
        write_text(summary)
        max_length = 500
        return render_template('summery.html', summary=transcript,history=history)
    else:
        return render_template('summery.html')

@app.route('/answer',methods=['GET','POST'])
def answer_question():
    # Get the question from the UI
    if request.method == 'POST':
        question = request.form['question']

        # Read text from text.txt file
        with open("text.txt", "r") as file:
            context = file.read()

        # Tokenize inputs
        inputs = tokenizer(question, context, return_tensors='pt',max_length=50)

        # Perform question answering
        outputs = model(**inputs)

        # Get answer
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

        # Find the tokens with the highest start and end scores
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1  # Add 1 because the end index is exclusive

        # Get the tokens from the input_ids and decode them
        answer_tokens = inputs['input_ids'][0][answer_start:answer_end]
        answer_tokens = tokenizer.convert_ids_to_tokens(answer_tokens, skip_special_tokens=True)
        answer = tokenizer.convert_tokens_to_string(answer_tokens)

        conversation = [{'question': question, 'answer': answer}]

        return render_template('chat.html', conversation=conversation)
    else:
        return render_template('chat.html', conversation=[])

   
    
# server the app when this file is run
if __name__ == '__main__':
    app.run()