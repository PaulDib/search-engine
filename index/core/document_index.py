'''
Provides classes to index single documents.
'''
from .utility import get_word_list, count_tokens, merge_dictionaries
import re


class CACMDocumentParser(object):
    def __init__(self, file_path=""):
        self._file_ptr = None
        self._file_path = file_path
        self._fields = ["\.I", "\.T", "\.W", "\.K", "\.B", "\.A", "\.N", "\.X", "\.K"]
        self._focus_fields = ["\.T", "\.W", "\.K"]
        self._id_marker = ".I"
        self._title_marker = "\.T"
        
    def get_documents(self):
        self._file_ptr = open(self._file_path, 'r') 
        document_content = ""
        i = 0
        document_start_pos = 0
        for i, line in enumerate(self._file_ptr):
            if line.startswith(self._id_marker):
                if document_content:
                    # Indexing previous document
                    doc = self.parse_document(document_content)
                    document_end_pos = i - 1
                    yield (document_start_pos, document_end_pos, doc)
                document_start_pos = i
                document_content = line
            document_content = document_content + "\n" + line

        # Handling last document.
        if document_content:
            doc = self.parse_document(document_content)
            document_end_pos = i - 1
            yield (document_start_pos, document_end_pos, doc)
        self._file_ptr.close()
        self._file_ptr = None

    def parse_document(self, document_content):
        '''Parses one document and returns document object.'''
        title = self._extract_title(document_content)
        content = self._extract_focus_content(document_content)
        doc_id = self._extract_doc_id(document_content)
        return StructuredDocument(doc_id, title, content)

    def _extract_title(self, content):
        '''Extracts the title from the whole content.'''
        return self._extract_field(self._title_marker, content).strip()

    def _extract_doc_id(self, content):
        '''Extracts the doc id from the content.'''
        return int(self._extract_field('\\' + self._id_marker, content))

    def _extract_focus_content(self, content):
        '''Extracts the interesting content.'''
        focus_content = ""
        for field in self._focus_fields:
            focus_content += " " + self._extract_field(field, content).strip()
        return focus_content

    def _extract_field(self, field_marker, content):
        '''Extracts a specified field.'''
        pattern = r'^(?:{0})(?P<extracted>.*?)(?:{1}|\Z)'.format(
            field_marker,
            "|".join(self._fields)
        )
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if not match:
            return ""
        return match.group('extracted')


class StructuredDocument(object):

    '''
    Class representing one structured document for read access.
    '''

    def __init__(self, doc_id, title, content):
        self._doc_id = doc_id
        self._title = title
        self._content = content

    def get_content(self):
        '''Returns the indexed content of the document.'''
        return self._content

    def get_title(self):
        '''Returns the field that was marked as title of the document.'''
        return self._title

    def get_doc_id(self):
        '''Returns the doc id of the document.'''
        return self._doc_id



class PlainDocument(object):

    '''
    Class representing a plain text (non structured) document for read access.
    '''

    def __init__(self, content):
        self._content = content

    def get_content(self):
        '''Returns the whole content of the document.'''
        return self._content


class DocumentIndex(object):

    '''
    Class containing the indexing result for one document.
    If provided with a indexConfig, the indexing will parse the document
    and filter stop words. Otherwise, indexing will be done on
    the whole content.
    '''

    def __init__(self, content, stop_words=None):
        self.word_count = {}
        self._maxword_count = -1
        if stop_words:
            self._stop_words = stop_words
        else:
            self._stop_words = []
        self._init_index(content)

    def get_word_count(self):
        '''Returns a dictionary with words and their counts.'''
        return self.word_count

    def _init_index(self, content):
        '''Indexes one document and populates word_count.'''
        self.word_count = self._compute_word_count(content)

    def _compute_word_count(self, content):
        '''Computes the word count for a string.'''
        return count_tokens(self._tokenize(content))

    def _tokenize(self, content):
        '''Returns an array of tokens (clean words) in a string.'''
        tokens = get_word_list(content, self._stop_words)
        return tokens
