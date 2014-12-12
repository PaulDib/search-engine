import re

def filterWords(wordList, stopWords):
    return [x for x in wordList if x not in stopWords]

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

def countTokens(tokens):
    '''Given a list of elements, counts the number of occurences of each element as a dictionary.'''
    result = {}
    for token in tokens:
        if token in result:
            result[token] = result[token] + 1
        else:
            result[token] = 1
    return result
