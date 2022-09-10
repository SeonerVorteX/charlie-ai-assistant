# SeoenerVorteX ~ 07/21/2022 ~ Charlie AI Assistant

import os
import sys
import time
import json
import nltk
import pyowm
import numpy
import random
import pickle
import tflearn
import oauthlib
import wikipedia
import webbrowser
import tensorflow
import win32gui
import win32con

# the_program_to_hide = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)

from charlie import *
from functions import *
from newsapi import NewsApiClient
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
sys.excepthook = sys.__excepthook__

charlie = Charlie()
charlie.set_voice_settings()

data = load_json("helpers/intents.json")

try:
    
    with open("datas/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])
        
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]
    
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    
    with open("datas/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

if file_exist("datas/model.tflearn.index"):
    
    model.load("datas/model.tflearn")
else:
    
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=False)
    model.save("datas/model.tflearn")

def main():
    os.system('cls')
    run = True
    sleep = False
    exception = False
    charlie.on_start()
    while run:
        exception_count = charlie.get_audio_exception_count
        if exception_count >= 5:
            if sleep == False:
                sleep = True
                charlie.sleep()
            
            text = charlie.get_audio(log=False).lower()
            if text == "":
                continue
            
            tag = classify(text, model, words, labels)
            if tag == "Callings":
                charlie.call()
                exception = False
                sleep = False
            else:
                continue
        else:
            text = charlie.get_audio(log=not(exception)).lower()
            if text == "":
                exception = True
                continue
            else:
                exception = False

            tag = classify(text, model, words, labels)
            charlie.get_audio_exception_count = 0

            if tag == None:
                charlie.did_not_undestand()
                continue

            charlie.speak(response(tag))

            intent = array_find(data["intents"], "tag", tag)

            if intent and len(intent["command"]):
                intent = None
                charlie.on_command(tag)

main()