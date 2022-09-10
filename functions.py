import os
import json
import nltk
import numpy
import random

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

def load_json(file):
    with open(file, "r") as f:
        return json.load(f)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words= [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = clean_up_sentence(s)
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def classify(sentence, model, words, labels):
    results = model.predict([bag_of_words(sentence, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index] > 0.8:
        return tag
    else:
        return None

def response(tag):
    data = load_json("helpers/intents.json")
    responses = []
    for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]

    if len(responses):
        return random.choice(responses)
    else:
        return ""

def array_random(list):
    return random.choice(list) 

def array_find(list, item, value):
    for i in list:
        if i[item] == value:
            return i
    return None

def array_some(list, item):
    return any(len(item) and item == i for i in list)

def array_all(list, item):
    return all(len(item) and item == i for i in list)

def array_has(list, item):
    return any(len(item) and item in i for i in list)

def array_has_any(list, items):
    for item in items:
        if item in list:
            return True
    return False

def array_has_all(list, items):
    for item in items:
        if item not in list:
            return False
    return True

def file_exist(path):
    return os.path.exists(path)

