from textblob import TextBlob
import unicodedata
import pandas as pd
import re
import nltk


def getSentiment(blob):
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def getNouns(text):
    blob = TextBlob(text)
    words = []

    for word, tag in blob.tags:
        if tag == 'NN':
            words.append(word)

    return words


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def get_stem(text):
    stemmer = nltk.porter.PorterStemmer()
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text


def getTags(df):
    tags_df = df.Tags.values.tolist()
    push_tag = ''
    tags = []
    for i in tags_df:
        for j in i:
            tags.append(j)
    tags = list(dict.fromkeys(tags))

    for tag in tags:
        push_tag += tag
        push_tag += ','

    return push_tag[: -1]


def sentenceEvaluation(text):
    sentences, sentiSentences = [], []
    sentence = ''
    text = text.replace('!', '.')
    text = text.replace('?', '.')
    text = text.replace(';', '.')

    sentences = text.split('.')

    for sentence in sentences:
        s = re.sub(r'\b\w{1,3}\b', '', sentence)
        s = remove_accented_chars(s)
        s = get_stem(s)
        s = re.sub(r'[^a-zA-z\"\'\s]', '', s)
        s = re.sub(r'[0-9]+', '', s)
        s = re.sub(' +', ' ', s)
        s = s.lower()
        s = TextBlob(s)
        s = s.correct()
        pol, sub = getSentiment(s)
        pol_abs = abs(pol)
        sentiSentences.append([str(s), pol, pol_abs, sub])
        dfS = pd.DataFrame(sentiSentences, columns=[
            'Sentence', 'Polarity', 'Absolute_polarity', 'Subjectivity'])
        dfS = dfS.sort_values(by='Absolute_polarity', ascending=False)
        dfS['Tags'] = dfS.Sentence.apply(getNouns)
        tags = getTags(dfS)

    return tags


def getSentimentPara(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity
