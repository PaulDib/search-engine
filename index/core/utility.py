'''
Provides general purpose functions.
'''
import re
from .constants import NORM_COUNT
from math import log, sqrt


def filter_words(word_list, stop_words):
    '''Removes stop_words from word_list'''
    return [x for x in word_list if x not in stop_words]


def split_content(content):
    '''Splits a string around spaces and non-alphanumeric characters'''
    return re.findall(r"[\w]+", content)


def merge_dictionaries(dict_a, dict_b):
    '''Merge two dictionaries by summing values'''
    res = dict_a
    for k in dict_b:
        if k in res:
            res[k] = res[k] + dict_b[k]
        else:
            res[k] = dict_b[k]
    return res


def get_word_list(content):
    '''Gets the list of words in a string'''
    content = re.sub(r'[^\w\s]', ' ', content)
    word_list = split_content(content)
    word_list = [x.lower() for x in word_list]
    return word_list


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


def compute_norm_count_for_word(word, vector):
    '''Gets the normalized count for one word in a vector.'''
    return vector[word][NORM_COUNT]


def compute_tfidf_for_word(word, vector, index):
    '''Computes the tf idf for a word in the vector against the index.'''
    return index.compute_tfidf_for_word(word, vector)


def compute_query_vector(query_words, statistic_function):
    '''
    Computes a vector representing a query
    given the words and a statistic to compute.
    '''
    query_vector = {}
    for word in query_words:
        query_vector[word] = statistic_function(word, query_words)
    return query_vector
 