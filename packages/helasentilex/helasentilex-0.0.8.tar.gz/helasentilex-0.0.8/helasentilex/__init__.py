import os

file_name = os.path.dirname(os.path.abspath(__file__)) + '/data'
fo = open(file_name, 'r', encoding='utf-8')
lines = fo.readlines()
fo.close()

sentiment_dict = {}
for line in lines:
    word, score = line.strip().split(',')
    sentiment_dict[word] = score

def sentiment(word):
    try:
        if word in sentiment_dict.keys():
            sentiment = int(sentiment_dict[word])
            return sentiment
        else:
            return 0
    except:
        return 0