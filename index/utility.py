import re
from math import log, sqrt


def filterWords(wordList, stop_words):
    return [x for x in wordList if x not in stop_words]


def splitContent(content):
    '''Splits a string around spaces and non-alphanumeric characters'''
    return re.findall(r"[\w]+", content)


def mergeDictionaries(a, b):
    '''Merge two dictionaries by summing values'''
    res = a
    for k in b:
        if k in res:
            res[k] = res[k] + b[k]
        else:
            res[k] = b[k]
    return res


def getWordList(content):
    '''Gets the list of words in a string'''
    wordList = splitContent(content)
    wordList = [x.lower() for x in wordList]
    return wordList


def count_tokens(tokens):
    '''
    Given a list of elements, counts the number of occurences
    of each element as a dictionary.
    '''
    result = {}
    for token in tokens:
        if token in result:
            result[token] = result[token] + 1
        else:
            result[token] = 1
    return result


def tf_idf(tf, df, doc_nbr):
    '''
    Computes tf idf.
    tf: frequency of a term in the document
    df: number of documents that contain the term
    doc_nbr: number of documents in the index
    '''
    if tf == 0:
        return 0
    return (log(tf + 1) / log(10)) * log(doc_nbr / df) / log(10)


def flatten(dic):
    '''
    Flatten a dictionary recursively.
    { "a": { "b": 0, "c": 1 } } should be flattened in { "a.b": 0, "a.c": 1 }
    '''
    res = {}
    if not isinstance(dic, dict):
        return dic
    for key in dic:
        if isinstance(dic[key], dict):
            flat_nested = flatten(dic[key])
            for deeper_key in flat_nested:
                concat_key = key + '.' + deeper_key
                res[concat_key] = flat_nested[deeper_key]
        else:
            res[key] = dic[key]
    return res


def norm(word_dict, weight_key=""):
    '''
    Computes the norm of a word vector.
    '''
    _sum = 0
    for word in word_dict:
        value = word_dict[word][weight_key] if weight_key else word_dict[word]
        _sum = _sum + value * value
    return sqrt(_sum)
