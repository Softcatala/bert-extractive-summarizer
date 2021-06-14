from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS
import nltk
from nltk import tokenize
from typing import List
import argparse
from summarizer import Summarizer, TransformerSummarizer
import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-model', dest='model', default='distilbert-base-uncased', help='The model to use')
    parser.add_argument('-transformer-type',
                        dest='transformer_type', default=None,
                        help='Huggingface transformer class key')
    parser.add_argument('-transformer-key', dest='transformer_key', default=None,
                        help='The transformer key for huggingface. For example bert-base-uncased for Bert Class')
    parser.add_argument('-greediness', dest='greediness', help='', default=0.45)
    parser.add_argument('-reduce', dest='reduce', help='', default='mean')
    parser.add_argument('-hidden', dest='hidden', help='', default=-2)
    ##parser.add_argument('-port', dest='port', help='', default=8080)
    ##parser.add_argument('-host', dest='host', help='', default='0.0.0.0')

    args = parser.parse_args()
    
    nltk.download('punkt')


    if args.transformer_type is not None:
        print(f"Using Model: {args.transformer_type}")
        assert args.transformer_key is not None, 'Transformer Key cannot be none with the transformer type'

        summarizer = TransformerSummarizer(
            transformer_type=args.transformer_type,
            transformer_model_key=args.transformer_key,
            hidden=int(args.hidden),
            reduce_option=args.reduce
        )

    else:
        print(f"Using Model: {args.model}")

        summarizer = Summarizer(
            model=args.model,
            hidden=int(args.hidden),
            reduce_option=args.reduce
        )

    #app.run(port=int(args.port))
    #app.run(host=args.host, port=int(args.port))



