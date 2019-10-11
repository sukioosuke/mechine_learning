import pandas as pd
import collections
import jieba
import re
import matplotlib.pyplot as plt

from functools import reduce

database = "../../data/news/sqlResult_1558435.csv"
dataframe = pd.read_csv(database, encoding='gb18030')
content = dataframe['content'].tolist()


def token(string):
    return ' '.join(i for i in re.findall('[\w|\d]+', string) if i.strip() != '' and i != '\n')


def cut(string): return list(jieba.cut(string))

ALL_TOKEN = []
TWO_GRAM_TOKEN = []
for a in content[:2000]:
    text = cut(token(str(a)))
    ALL_TOKEN += text
    for i in range(len(text[:-1])):
        TWO_GRAM_TOKEN += [text[i] + text[i + 1]]

words = collections.Counter(ALL_TOKEN)
one_gram_sum = sum([k for w, k in words.most_common()])


# def language_model_one_gram(sentence):
#     percent = 1.0
#     eps = 1 / sum
#     for i in jieba.cut(token(sentence)):
#         if words[i] is None:
#             percent *= eps
#         percent *= words[i] / sum
#     return percent
#
#
# print(language_model_one_gram("我想吃个苹果"))

two_gram_words = collections.Counter(TWO_GRAM_TOKEN)
two_gram_sum = sum([f for w, f in two_gram_words.most_common()])


def language_model_two_gram(sentence):
    percent = 1.0
    eps = 1 / two_gram_sum
    words = cut(token(sentence))
    for index in range(len(words[:-1])):
        if (words[index] + words[index + 1]) in two_gram_words:
            percent *= two_gram_words[words[index] + words[index + 1]] / two_gram_sum

        else:
            percent *= eps

    return percent


