'''
Provides a REPL client for the index package.
'''
import os
import time
import traceback
from ...core.index import Index
from ...core.index_config import IndexConfig
from ...core.index_serializer import IndexSerializer
from ...core.boolean_query import BooleanQuery
from ...core.vectorial_query import VectorialQueryTfIdf, VectorialQueryNormCount
from .command_line import CommandLine


class ReplClient(object):

    '''Read-Eval-Print-Loop client for the index.'''

    def __init__(self, working_dir=None):
        if working_dir:
            self._working_dir = working_dir
        else:
            self._working_dir = os.getcwd()
        self.index = None
        self._actions = {
            'createIndex': CreateIndexAction,
            'boolean': BooleanQueryAction,
            'exit': EmptyAction,
            'saveIndex':  SaveIndexAction,
            'loadIndex': LoadIndexAction,
            'tfidfVectorial': VectorialQueryTfidfAction,
            'normCountVectorial': VectorialQueryNormCountAction
        }
        self._command_line = CommandLine(
            autocomplete_actions=self._actions.keys())
        self._start_repl()

    def _start_repl(self):
        '''Starts the REPL and prompts the user.'''
        user_input = ""
        print("Starting interactive environment in directory "
              + self._working_dir)
        while user_input != "exit":
            user_input = self._command_line.read_input("> ")
            if not user_input:
                continue
            try:
                action = self._parse_input(user_input)
                action.execute()
            except Exception as exc:
                print("Error: " + str(exc))
                print(traceback.format_exc())
        print("Exiting...")

    def _parse_input(self, user_input):
        '''
        Parses user input and returns corresponding action.
        '''
        split = user_input.split()
        command = split[0]
        arguments = split[1:] if len(split) > 1 else []
        if command in self._actions:
            action_factory = self._actions[command]
            return action_factory(self, arguments)
        else:
            raise ValueError("<" + command + "> unknown command.")


class Action(object):

    '''Abstract action for the REPL client.'''

    def execute(self):
        '''Executes the action a prints results to the user.'''
        raise NotImplementedError("Wrong action.")

    def help(self):
        '''Display help text to the user regarding this action.'''
        pass


class EmptyAction(Action):

    def __init__(self, client, arguments):
        pass

    def execute(self):
        pass


class CreateIndexAction(Action):

    def __init__(self, client, arguments):
        self._client = client
        if len(arguments) < 1 or len(arguments) > 2:
            raise ValueError(self.help())
        self._data_files = arguments[0].split(";")
        self._stop_words_file = arguments[1] if len(arguments) == 2 else ""

    def execute(self):
        index_config = IndexConfig(self._stop_words_file)
        print("Indexing files...")
        t_start = time.time()
        self._client.index = Index(self._data_files, index_config)
        print("Index has been created in " +
              str(time.time() - t_start) + " seconds.")

    def help(self):
        return '''Wrong use.
        Example: createIndex data_file1;data_file2 stop_word_file'''


class BooleanQueryAction(Action):

    def __init__(self, client, arguments):
        if not arguments:
            raise ValueError(self.help())
        if not client.index:
            raise ValueError("Create or load an index first.")
        query_text = "".join(arguments)
        self._query = BooleanQuery(query_text)
        self._query.set_index(client.index)
        self.index = client.index

    def execute(self):
        t_start = time.time()
        docs = self._query.execute()
        duration = time.time() - t_start
        print("Query executed in " + str(duration) +
              " seconds and returned " + str(len(docs)) + " results.")
        iterator = iter(docs)
        for i in range(0, min(len(docs), 10)):
            doc_id = next(iterator)
            document = self.index.document_by_id(doc_id)
            print("<" + str(doc_id) + "> - " + document.get_title())
        if len(docs) > 10:
            print("More than 10 results, the list has been truncated. \
                Here is the full list of document ids:")
            print(docs)

    def help(self):
        return '''Wrong use.
        Example: boolean (word1 * !word2) + word3'''


class VectorialQueryAction(Action):

    '''Abstract class for vectorial query action.'''

    def __init__(self, client, arguments):
        if not arguments:
            raise ValueError(self.help())
        if not client.index:
            raise ValueError("Create or load an index first.")
        self.index = client.index
        self._query = None

    def execute(self):
        t_start = time.time()
        docs = self._query.execute(self.index)
        duration = time.time() - t_start
        print("Query executed in " + str(duration) +
              " seconds and returned " + str(len(docs)) + " results.")
        for (k, value) in docs[0:10]:
            document = self.index.document_by_id(k)
            print("<" + str(k) + "> - " + document.get_title())
        if len(docs) > 10:
            print("More than 10 results, the list has been truncated. \
                Here is the list of the 10 first results with weights:")
        print(docs[0:10])

    def help(self):
        pass

class VectorialQueryTfidfAction(VectorialQueryAction):

    def __init__(self, client, arguments):
        super(VectorialQueryTfidfAction, self).__init__(client, arguments)
        query_text = " ".join(arguments)
        self._query = VectorialQueryTfIdf(query_text)

    def help(self):
        return '''Wrong use.
        Example: tfidfVectorial this is a vectorial query'''


class VectorialQueryNormCountAction(VectorialQueryAction):

    def __init__(self, client, arguments):
        super(VectorialQueryNormCountAction, self).__init__(client, arguments)
        query_text = " ".join(arguments)
        self._query = VectorialQueryNormCount(query_text)

    def help(self):
        return '''Wrong use.
        Example: normCountVectorial this is a vectorial query'''


class SaveIndexAction(Action):

    def __init__(self, client, arguments):
        if not arguments:
            raise ValueError(self.help())
        if not client.index:
            raise ValueError("Create or load an index first.")
        self._index = client.index
        self._path = arguments[0]

    def execute(self):
        print("Saving index...")
        start_time = time.time()
        IndexSerializer.save_to_file(self._index, self._path)
        dur = time.time() - start_time
        print("Index saved in " + str(dur) + " seconds.")

    def help(self):
        return '''Wrong use.
        Example: saveIndex path/to/output/file'''


class LoadIndexAction(Action):

    def __init__(self, client, arguments):
        if not arguments:
            raise ValueError(self.help())
        self._client = client
        self._path = arguments[0]

    def execute(self):
        print("Loading index...")
        start_time = time.time()
        self._client.index = IndexSerializer.load_from_file(self._path)
        dur = time.time() - start_time
        print("Index loaded in " + str(dur) + " seconds.")

    def help(self):
        return '''Wrong use.
        Example: saveIndex path/to/output/file'''
