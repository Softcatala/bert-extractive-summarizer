from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS
import nltk
from nltk import tokenize
from typing import List
import argparse
from summarizer import Summarizer, TransformerSummarizer
import datetime

app = Flask(__name__)
CORS(app)

_summarizer = None

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
    return 'Servei actiu!'

@app.route('/summarize_by_sentence', methods=['POST'])
def convert_raw_text_by_sent():

    global _summarizer
#    num_sentences = int(request.args.get('num_sentences', 5))

    start_time = datetime.datetime.now()

    min_length = int(request.args.get('min_length', 25))
    max_length = int(request.args.get('max_length', 500))

    data = request.form['text']
    num_sentences = int(request.form.get('num_sentences', 5))

    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))

    parsed = Parser(data).convert_to_paragraphs()
    summary = _summarizer(parsed, num_sentences=num_sentences, min_length=min_length, max_length=max_length)

    time_used = datetime.datetime.now() - start_time

    return jsonify({
        'summary': summary,
        'time' : str(time_used)
    })


def init():
    global _summarizer

    model = 'bert-base-uncased'
    transformer_type = None
    transformer_key = None
    greediness = 0.45
    reduce = 'mean'
    hidden = -2

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

    #app.run(port=int(args.port))
    #app.run(host=args.host, port=int(args.port))


if __name__ == '__main__':
#    app.debug = True
    init()
    app.run()

if __name__ != '__main__':
    init()

