import os
import time
import traceback
from .index import Index
from .index_config import IndexConfig
from .index_serializer import IndexSerializer
from .boolean_query import BooleanQuery
from .vectorial_query import VectorialQuery
from .command_line import CommandLine


class ReplClient:

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
            'vectorial': VectorialQueryAction
        }
        self._command_line = CommandLine(
            autocomplete_actions=self._actions.keys())
        self._startREPL()

    def _startREPL(self):
        usrInput = ""
        print(
            "Starting interactive environment in directory " + self._working_dir)
        while(usrInput != "exit"):
            usrInput = self._command_line.readInput("> ")
            if not usrInput:
                continue
            try:
                action = self._parseInput(usrInput)
                action.execute()
            except Exception as e:
                print("Error: " + str(e))
                print(traceback.format_exc())
        print("Exiting...")

    def _parseInput(self, usrInput):
        split = usrInput.split()
        command = split[0]
        arguments = split[1:] if len(split) > 1 else []
        if command in self._actions:
            actionFactory = self._actions[command]
            return actionFactory(self, arguments)
        else:
            raise ValueError("<" + command + "> unknown command.")


class Action:

    def execute(self):
        raise NotImplementedError("Wrong action.")


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
        self._stop_words_file = arguments[2] if len(arguments) == 2 else ""

    def execute(self):
        indexConfig = IndexConfig(self._stop_words_file)
        print("Indexing files...")
        t_start = time.time()
        self._client.index = Index(self._data_files, indexConfig)
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
        queryText = "".join(arguments)
        self._query = BooleanQuery(queryText)
        self._query.set_index(client.index)
        self.index = client.index

    def execute(self):
        t_start = time.time()
        docs = self._query.execute()
        duration = time.time() - t_start
        print("Query executed in " + str(duration) +
              " seconds and returned " + str(len(docs)) + " results.")
        it = iter(docs)
        for i in range(0, min(len(docs), 10)):
            docId = next(it)
            document = self.index.documentById(docId)
            print("<" + str(docId) + "> - " + document.get_title())
        if len(docs) > 10:
            print(
                "More than 10 results, the list has been truncated. Here is the full list of document ids:")
            print(docs)

    def help(self):
        return '''Wrong use.
        Example: boolean (word1 * !word2) + word3'''


class VectorialQueryAction(Action):

    def __init__(self, client, arguments):
        if not arguments:
            raise ValueError(self.help())
        if not client.index:
            raise ValueError("Create or load an index first.")
        queryText = " ".join(arguments)
        self._query = VectorialQuery(queryText)
        self.index = client.index

    def execute(self):
        t_start = time.time()
        docs = self._query.execute(self.index)
        duration = time.time() - t_start
        print("Query executed in " + str(duration) +
              " seconds and returned " + str(len(docs)) + " results.")
        for (k, v) in docs[0:10]:
            document = self.index.documentById(k)
            print("<" + str(k) + "> - " + document.get_title())
        if len(docs) > 10:
            print(
                "More than 10 results, the list has been truncated. Here is the full list of document ids:")
        print(docs)

    def help(self):
        return '''Wrong use.
        Example: vectorial this is a vectorial query'''


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
        t0 = time.time()
        IndexSerializer.save_to_file(self._index, self._path)
        dur = time.time() - t0
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
        t0 = time.time()
        self._client.index = IndexSerializer.load_from_file(self._path)
        dur = time.time() - t0
        print("Index loaded in " + str(dur) + " seconds.")

    def help(self):
        return '''Wrong use.
        Example: saveIndex path/to/output/file'''
