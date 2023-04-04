from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

model_name = "philschmid/bart-large-cnn-samsum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)



@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.json['text']
    input_ids = tokenizer(text, return_tensors='pt', padding=True, truncation=True)['input_ids']
    summary_ids = model.generate(input_ids, max_length=61, num_beams=2, length_penalty=1.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    text = "The U.S. economy added 559,000 jobs in May, below economists' estimates and a sign the recovery from the pandemic is progressing at a slower pace than expected."
    response = requests.post('http://localhost:5000/summarize', json={'text': text})
    summary = response.json()['summary']
    print(summary)
    return jsonify({'summary': summary})