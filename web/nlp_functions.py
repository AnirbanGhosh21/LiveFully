from textblob import TextBlob
import re
from nltk import tokenize
import pandas as pd


def analyzeText(text):
    blob = TextBlob(text)
    blob = blob.correct()
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    print(phrase)
    return phrase


def splitPara(paragraph):
    sentences = tokenize.sent_tokenize(paragraph)
    sentences_term = []
    for sentence in sentences:
        if sentence[-1] == '.' or sentence[-1] == '?' or sentence[-1] == '!':
            sentences_term.append(decontracted(sentence[:-1]))
        else:
            sentences_term.append(decontracted(sentence))
    return sentences_term


for sentence in splitPara('I woke up not being able to breathe well. I couldn’t think or talk well because I was putting all of my energy toward breathing. There was also a really hard pressure on my chest that would not go away. That night, I went to the ER because my difficulty breathing worsened. The hospital staff immediately took me in and plugged me into an oxygen machine.'):
    print(sentence, analyzeText(sentence))
