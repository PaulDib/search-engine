'''
Provides general purpose functions.
'''
import re
from math import log, sqrt
from nltk import PorterStemmer

_stemmer = PorterStemmer()

def filter_words(word_list, stop_words):
    '''Removes stop_words from word_list'''
    return [x for x in word_list if x not in stop_words]


def split_content(content):
    '''Splits a string around spaces and non-alphanumeric characters'''
    return re.findall(r"[\w]+", content)


def merge_dictionaries(dict_a, dict_b="", merging_func=lambda x, y: x + y):
    '''Merge two dictionaries by summing values'''
    res = dict_a if len(dict_a) > len(dict_b) else dict_b
    iterated = dict_b if len(dict_a) > len(dict_b) else dict_a
    for k in iterated:
        if k in res:
            res[k] = merging_func(res[k], iterated[k])
        else:
            res[k] = iterated[k]
    return res


def get_word_list(content, stop_words):
    '''Gets the list of words in a string'''
    if not stop_words:
        stop_words = []
    content = re.sub(r'[^\w\s]', ' ', content).lower()
    word_list = split_content(content)
    word_list = filter_words(word_list, stop_words)
    word_list = [tokenize(x) for x in word_list]
    return word_list


def tokenize(word):
    '''
    Return the token corresponding to the input word.
    '''
    return _stemmer.stem_word(word.lower())


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


def tf_idf(term_frequency, document_frequency, doc_nbr):
    '''
    Computes term frequency - inverse document frequency.
    term_frequency: frequency of a term in the document
    document_frequency: number of documents that contain the term
    doc_nbr: number of documents in the index
    '''
    if term_frequency == 0:
        return 0
    return (log(term_frequency + 1) / log(10)) \
        * log(doc_nbr / document_frequency) / log(10)


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


def scalar_product(vector_a, vector_b):
    '''
    Computes the scalar product of two dictionaries.
    '''
    result = 0
    if len(vector_a) > len(vector_b):
        tmp = vector_b
        vector_b = vector_a
        vector_a = tmp
    for word in vector_a:
        if word in vector_b:
            result += vector_a[word]*vector_b[word]
    return result


def probabilistic_weight(term_prob):
    '''
    Computes the probabilistic weight for a word.
    '''
    return log(term_prob/(1 - term_prob))
