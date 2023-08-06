#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 09:02:20 2020

@author: nageshsinghchauhan
"""
import base64
import os
import spacy
from spacy import displacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pickle
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import numpy as np
import string
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
nlp = spacy.load('en_core_web_sm')

class NaturalLanguage:
    
    def pos_tagger(params):
        try:
            text = params
            doc = nlp(text)
            response = {}
            pos_response = {}
            for token in doc:
                pos_response[token.text] = token.tag_
            response["result"] = pos_response
            response["text"] = text
            return response
        except Exception as e:
            print("Exception generated inside pos_tagger method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)
    
    
    
    
    
    def ner_tagger(params):
        try:
            text = params
            doc = nlp(text)
            response = {}
            ner_response = {}
            person_details = []
            org_details = []
            for ent in doc.ents:
                ner_response[str(ent)] = ent.label_
            response["result"] = ner_response
            response["text"] = text
            response["persons"] = person_details
            response["organizations"] = org_details
            return response
        except Exception as e:
            print("Exception generated inside ner_tagger method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)
    
    
    
    
    def parser(params):
        try:
            text = params
            doc = nlp(text)
            response = {}
            dependency_response = {}
            for token in doc:
                dependency_response[str(token.text)] = {"dep": token.dep_,
                                                        "headText": token.head.text,
                                                        "headPOS": token.head.pos_,
                                                        "children": [str(child) for child in token.children]
                                                        }
            response["result"] = dependency_response
            response["text"] = text
            return dependency_response
        except Exception as e:
            print("Exception generated inside parser method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)
    
    
    def sentiment(params):
        try:
            text = params
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(text)
            response = {}
            if scores["compound"] > 0:
                emotion = "POSITIVE"
                polarity = 3
            elif scores["compound"] < 0:
                emotion = "NEGATIVE"
                polarity = 1
            else:
                emotion = "NEUTRAL"
                polarity = 0
            response["emotion"] = emotion
            response["text"] = text
            response["polarity"] = polarity
            response["scores"] = scores
            return response
        except Exception as e:
            print("Exception generated inside sentiment method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)
    
    
    
    
        def parser_svg(self,params):
            try:
                text = params
                doc = nlp(text)
                svg = displacy.render(doc, style="dep")
                # svg2png(bytestring=svg, write_to='output.png')
                with open('output.png', "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                return encoded_string
            finally:
                os.remove('output.png')
    def clean_text(text):
        try:
    
    
            text = text.translate(string.punctuation)
    
    
            text = text.lower().split()
    
            stops = set(stopwords.words("english"))
            text = [w for w in text if not w in stops and len(w) >= 3]
    
            text = " ".join(text)
    
    
            text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
            text = re.sub(r"what's", "what is ", text)
            text = re.sub(r"\'s", " ", text)
            text = re.sub(r"\'ve", " have ", text)
            text = re.sub(r"n't", " not ", text)
            text = re.sub(r"i'm", "i am ", text)
            text = re.sub(r"\'re", " are ", text)
            text = re.sub(r"\'d", " would ", text)
            text = re.sub(r"\'ll", " will ", text)
            text = re.sub(r",", " ", text)
            text = re.sub(r"\.", " ", text)
            text = re.sub(r"!", " ! ", text)
            text = re.sub(r"\/", " ", text)
            text = re.sub(r"\^", " ^ ", text)
            text = re.sub(r"\+", " + ", text)
            text = re.sub(r"\-", " - ", text)
            text = re.sub(r"\=", " = ", text)
            text = re.sub(r"'", " ", text)
            text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
            text = re.sub(r":", " : ", text)
            text = re.sub(r" e g ", " eg ", text)
            text = re.sub(r" b g ", " bg ", text)
            text = re.sub(r" u s ", " american ", text)
            text = re.sub(r"\0s", "0", text)
            text = re.sub(r" 9 11 ", "911", text)
            text = re.sub(r"e - mail", "email", text)
            text = re.sub(r"j k", "jk", text)
            text = re.sub(r"\s{2,}", " ", text)
    
    
    
            return text
        except Exception as e:
            print("Exception generated inside clean_text method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)
    
    
    def toxic_comment_detect(text):
        try:
            maxlen = 50
            embed_dim = 100
            max_words = 20000
            print('inside detect function before cleaning')
            text=clean_text(str(text))
            print(text)
            print(type(text))
            with open(os.getcwd()+'/resources/tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            ls=[]
            ls.append(text)
            data = tokenizer.texts_to_sequences(ls)
            #print('tokenized data-',data)
            data = pad_sequences(data, maxlen=maxlen, padding='post')
            #print('padded-seq',data)
            model=load_model(os.getcwd()+'/resources/Cyber_bullying-LSTM-multi-class')
            pred=model.predict(data)
            print(pred)
            #print(model.summary())
            dt=tokenizer.word_index
            print(np.argmax(pred))
            sample='nothing detected'
            if np.argmax(pred)==1:
                sample='racism'
            elif np.argmax(pred)==2:
                sample='sexism'
            return sample
        except Exception as e:
            print("Exception generated inside toxic_comment_detect method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)
    
