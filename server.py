from flask import Flask
from flask import request, jsonify, abort, make_response, Response
from flask_cors import CORS
from nltk import tokenize
from typing import List
import argparse
from summarizer import Summarizer, TransformerSummarizer
import datetime
import torch
import os
from langdetect import detect
from usage import Usage
import json
import logging
import logging.handlers


app = Flask(__name__)
CORS(app)

_summarizer = None

def init_logging():
    logfile = 'summarizer-service.log'

    LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
#    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logger = logging.getLogger()
    hdlr = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(LOGLEVEL)

    console = logging.StreamHandler()
    console.setLevel(LOGLEVEL)
    logger.addHandler(console)


class Parser(object):

    def __init__(self, raw_text: bytes):
        self.all_data = raw_text.split('\n')

    def __isint(self, v) -> bool:
        try:
            int(v)
            return True
        except:
            return False

    def __should_skip(self, v) -> bool:
        return self.__isint(v) or v == '\n' or '-->' in v

    def __process_sentences(self, v) -> List[str]:
        sentence = tokenize.sent_tokenize(v)
        return sentence

    def save_data(self, save_path, sentences) -> None:
        with open(save_path, 'w') as f:
            for sentence in sentences:
                f.write("%s\n" % sentence)

    def run(self) -> List[str]:
        total: str = ''
        for data in self.all_data:
            if not self.__should_skip(data):
                cleaned = data.replace('&gt;', '').replace('\n', '').strip()
                if cleaned:
                    total += ' ' + cleaned
        sentences = self.__process_sentences(total)
        return sentences

    def convert_to_paragraphs(self) -> str:
        sentences: List[str] = self.run()
        return ' '.join([sentence.strip() for sentence in sentences]).strip()

@app.route('/hello', methods=['GET'])
def hello_world():
    threads = torch.get_num_threads()
    return f'Servei actiu! Fils {threads}'

def _is_catalan_language(text):
    lang = detect(text)
    print(f"lang: {lang}")
    return lang == 'ca'

def json_answer(data, status = 200):
    json_data = json.dumps(data, indent=4, separators=(',', ': '))
    resp = Response(json_data, mimetype='application/json', status = status)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/stats/', methods=['GET'])
def stats():
    requested = request.args.get('date')
    date_requested = datetime.datetime.strptime(requested, '%Y-%m-%d')
    usage = Usage()
    result = usage.get_stats(date_requested)

    return json_answer(result)



@app.route('/summarize_by_sentence', methods=['POST'])
def convert_raw_text_by_sent():

    global _summarizer

    start_time = datetime.datetime.now()

    min_length = int(request.args.get('min_length', 25))
    max_length = int(request.args.get('max_length', 500))

    data = request.form['text']
    num_sentences = int(request.form.get('num_sentences', 5))

    data_len = len(data)
    if data_len > 64000:
        return jsonify({
            'summary': 'El text és massa larg pel nostre maquinari per poder-lo resumir',
            'time' : str(datetime.datetime.now() - start_time)
        })

    if _is_catalan_language(data) == False:
        return jsonify({
            'summary': 'Cal que el text sigui en català.',
            'time' : str(datetime.datetime.now() - start_time)
        })

    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))

    parsed = Parser(data).convert_to_paragraphs()
    summary = _summarizer(parsed, num_sentences=num_sentences, min_length=min_length, max_length=max_length)

    time_used = datetime.datetime.now() - start_time
    words = len(data.split(' '))
    usage = Usage()
    usage.log(words, time_used)

    return jsonify({
        'summary': summary,
        'time' : str(datetime.datetime.now() - start_time)
    })


def init():
    global _summarizer

    model = 'distilbert-base-uncased'
    transformer_type = None
    transformer_key = None
    greediness = 0.45
    reduce = 'mean'
    hidden = -2

    if 'THREADS' in os.environ:
        print("Set threads!")
        num_threads = int(os.environ['THREADS'])
        torch.set_num_threads(num_threads)

    if transformer_type is not None:
        print(f"Using Model: {transformer_type}")
        assert transformer_key is not None, 'Transformer Key cannot be none with the transformer type'

        _summarizer = TransformerSummarizer(
            transformer_type=transformer_type,
            transformer_model_key=transformer_key,
            hidden=int(hidden),
            reduce_option=reduce
        )

    else:
        print(f"Using Model: {model}")


        _summarizer = Summarizer(
            model=model,
            hidden=int(hidden),
            reduce_option=reduce
        )

    threads = torch.get_num_threads()
    print(f"threads: {threads}")
    #app.run(port=int(args.port))
    #app.run(host=args.host, port=int(args.port))



if __name__ == '__main__':
#    app.debug = True
    init_logging()
    init()

if __name__ != '__main__':
    init_logging()
    init()
