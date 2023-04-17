from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, jsonify, request, render_template
from flask.helpers import send_file
import requests

app = Flask(__name__)

model_name = "philschmid/bart-large-cnn-samsum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

@app.route('/')
def indexPage():
     return render_template("index.html")

# @app.route('/summarize', methods=['POST'])
# def summarize():
#     text = request.json['text']
#     input_ids = tokenizer(text, return_tensors='pt', padding=True, truncation=True)['input_ids']
#     summary_ids = model.generate(input_ids, max_length=61, num_beams=2, length_penalty=1.0, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     text = "The U.S. economy added 559,000 jobs in May, below economists' estimates and a sign the recovery from the pandemic is progressing at a slower pace than expected."
#     response = requests.post('http://localhost:5000/summarize', json={'text': text})
#     summary = response.json()['summary']
#     summary=jsonify({'summary': summary})
#     return "<p>{summary}</p>"
# @app.route('/summarize', methods=['POST'])
# def summarize():
#     summary = request.json['text']
#     result=my_function(summary)
#     return jsonify({'summary': result}) 

def my_function(text):
    input_ids = tokenizer(text, return_tensors='pt', padding=True, truncation=True)['input_ids']
    summary_ids = model.generate(input_ids)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        summary = request.json['text']
        if not summary:
            raise ValueError('Input text is empty')
        result = my_function(summary)
        if not result:
            raise ValueError('Unable to generate summary')
        return jsonify({'summary': result})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run()