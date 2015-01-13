'''
Provides document the general document parser structure
along with parsers for different types of documents.
'''
import re
from .document_index import StructuredDocument

class DocumentParser(object):

    '''
    Contains base code for parsing multiple documents
    in a file.
    '''

    def __init__(self, file_path=""):
        self._file_ptr = None
        self._file_path = file_path
        self._start_marker = None

    def get_documents(self):
        '''
        Generator.
        Iterates over all the documents in the file.
        '''
        self._file_ptr = open(self._file_path, 'r')
        document_content = ""
        i = 0
        document_start_pos = 0
        started = False
        for i, line in enumerate(self._file_ptr):
            if line.startswith(self._start_marker):
                if document_content and started:
                    # Indexing previous document
                    doc = self.parse_document(document_content)
                    document_end_pos = i - 1
                    yield (document_start_pos, document_end_pos, doc)
                document_start_pos = i
                document_content = line
                started = True
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

        pass

    def _extract_focus_content(self, content):
        '''Extracts the interesting content.'''
        pass

    def _extract_doc_id(self, content):
        '''Extracts the interesting content.'''
        pass


class INEXDocumentParser(DocumentParser):

    '''Contains the INEX document parsing logic.'''

    def __init__(self, file_path=""):
        super().__init__(file_path)
        self._start_marker = '<article>'
        self._id_pattern = r'<name id="(?P<id>\d+)">'
        self._title_pattern = r'<name.*>(?P<title>.+)</name>'

    def _extract_title(self, content):
        '''Extracts the title from the whole content.'''
        match = re.search(self._title_pattern, content)
        if not match:
            return ""
        return match.group("title")

    def _extract_focus_content(self, content):
        '''Extracts the interesting content.'''
        content = re.sub(r'<.*?>', '', content)
        return content

    def _extract_doc_id(self, content):
        '''Extracts the interesting content.'''
        match = re.search(self._id_pattern, content)
        if not match:
            return ""
        return int(match.group("id"))


class CACMDocumentParser(DocumentParser):

    '''Contains the CACM document parsing logic.'''

    def __init__(self, file_path=""):
        super().__init__(file_path)
        self._fields = [r"\.I", r"\.T", r"\.W", r"\.K", r"\.B", r"\.A", r"\.N",
                        r"\.X", r"\.K"]
        self._focus_fields = [r"\.T", r"\.W", r"\.K"]
        self._start_marker = r".I"
        self._title_marker = r"\.T"

    def _extract_title(self, content):
        '''Extracts the title from the whole content.'''
        return self._extract_field(self._title_marker, content).strip()

    def _extract_doc_id(self, content):
        '''Extracts the doc id from the content.'''
        return int(self._extract_field('\\' + self._start_marker, content))

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
        options = re.IGNORECASE | re.MULTILINE | re.DOTALL
        match = re.search(pattern, content, options)
        if not match:
            return ""
        return match.group('extracted')
