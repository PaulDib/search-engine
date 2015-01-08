'''
Generate statistics for all models on the index.
'''
from math import ceil
from pylab import *
import time
from ...core.index import Index
from ...core.index_config import IndexConfig
from ...core.vectorial_query import VectorialQueryTfIdf, VectorialQueryNormCount, VectorialQueryProbabilistic


def generate_recall_precision_graph(x_data, y_data, chart_title, output_folder):
    '''
    Generates a graph with x axis labelled as recall and y axis as precision.
    '''
    plot(x_data, y_data)
    xlabel('recall')
    ylabel('precision')
    title(chart_title)
    grid(True)
    if output_folder:
        savefig(output_folder + '/' + chart_title + '.png')


class StatsGenerator(object):

    '''
    Generates statistics for all models available
    in the core package.
    '''

    def __init__(self):
        self._data_file_path = ""
        self._stop_words_file_path = ""
        self._output_folder = ""
        self._queries_path = ""
        self._query_results_path = ""
        self._iterations = 100

    def set_query_path(self, queries_path, query_results_path):
        '''
        Sets the path to the query text file and the expected results file.
        '''
        self._queries_path = queries_path
        self._query_results_path = query_results_path

    def set_index_path(self, data_file_path, stop_words_file_path):
        '''
        Sets the path to data files and stop word file used by the index.
        '''
        self._data_file_path = data_file_path
        self._stop_words_file_path = stop_words_file_path

    def set_output_folder(self, output_folder):
        '''
        Sets the folder that will contain generated reports.
        '''
        self._output_folder = output_folder

    def set_iterations(self, iterations):
        '''
        Sets the number of times that the requests will be
        repeated to create the recall/precision graph.
        '''
        self._iterations = iterations

    def compute_statistics(self):
        '''
        Compute statistics on the index and saves results.
        '''
        print('Indexing...')
        start_time = time.time()
        config = IndexConfig(self._stop_words_file_path)
        index = Index(self._data_file_path, config)
        print('Indexing done in {0:.4f} seconds.'.format(time.time() - start_time))

        print('Reading queries and expected results...')
        queries = self._read_queries()
        expected = self._read_expected_results()
        print('{0} queries found. Each model will run {0} queries.'.format(
            len(queries),
            self._iterations*len(queries)
            ))

        print('Running queries...')
        start_time = time.time()
        generator = RecallPrecisionGenerator(index, VectorialQueryTfIdf, queries, expected)
        (recall, prec) = generator.generate(self._iterations)
        generate_recall_precision_graph(recall, prec, 'tfidf', self._output_folder)
        print('TFIDF queries ran in {0:.4f} seconds.'.format(time.time() - start_time))

        start_time = time.time()
        generator = RecallPrecisionGenerator(index, VectorialQueryNormCount, queries, expected)
        (recall, prec) = generator.generate(self._iterations)
        generate_recall_precision_graph(recall, prec, 'normalized_frequency', self._output_folder)
        print('Normalized freq. queries ran in {0:.4f} seconds.'.format(time.time() - start_time))

        start_time = time.time()
        generator = RecallPrecisionGenerator(index, VectorialQueryProbabilistic, queries, expected)
        (recall, prec) = generator.generate(self._iterations)
        generate_recall_precision_graph(recall, prec, 'probabilistic', self._output_folder)
        print('Probabilistic queries ran in {0:.4f} seconds.'.format(time.time() - start_time))

    def _read_queries(self):
        '''
        Read the queries that will be used to compute statistics.
        '''
        queries = {}
        query_id = 0
        with open(self._queries_path) as file_ptr:
            for line in file_ptr:
                if line.startswith('.I'):
                    query_id = int(line.split(" ")[1])
                elif line.startswith('.W'):
                    query_buffer = ""
                elif line.startswith('.N'):
                    queries[query_id] = query_buffer
                else:
                    query_buffer = query_buffer + line
        return queries


    def _read_expected_results(self):
        '''
        Read the expected results corresponding to the queries.
        '''
        expected = {}
        with open(self._query_results_path) as file_ptr:
            for line in file_ptr:
                splitted = line.split(" ")
                query_id = int(splitted[0])
                expected_doc = int(splitted[1])
                if query_id in expected:
                    expected[query_id].append(expected_doc)
                else:
                    expected[query_id] = [expected_doc]
        return expected


class RecallPrecisionGenerator(object):

    '''Generates recall-precision graph against test data.'''

    def __init__(self, index, query_type, queries, expected):
        self._index = index
        self._query_type = query_type
        self._queries = queries
        self._expected = expected
        self._results = {}

    def generate(self, iterations):
        '''
        Generates (recall_list, prec_list) that give the results of
        several computations averaged over all the test requests.
        '''
        average_prec_list = []
        average_recall_list = []

        for percentage in range(1, iterations):
            average_prec = 0
            average_recall = 0
            perc = int(ceil(percentage / iterations * 100))
            for (query_id, _) in self._queries.items():
                (recall, prec) = self._compute_recall_and_precision(query_id, perc)
                average_recall = average_recall + recall
                average_prec = average_prec + prec
            average_recall = average_recall / len(self._queries)
            average_prec = average_prec / len(self._queries)
            average_recall_list.append(average_recall)
            average_prec_list.append(average_prec)

        return (average_recall_list, average_prec_list)

    def _compute_recall_and_precision(self, query_id, percentage):
        '''
        Computes recall and precision for a single query.
        Percentage argument tells how many results should be considered.
        '''
        pertinent = self._expected[query_id] if query_id in self._expected else []
        pertinent_len = len(pertinent)

        query_results = self._get_query_results(query_id)
        results_len = len(query_results)

        top = int(ceil(results_len*percentage/100))
        query_results = query_results[0:top]
        results_len = top
        pertinent_found = len([k for k in pertinent if k in [x for (x, y) in query_results]])

        recall = pertinent_found / pertinent_len if pertinent_len > 0 else 1.0
        precision = pertinent_found / results_len
        return (recall, precision)

    def _get_query_results(self, query_id):
        '''
        Gets the result of a query.
        Does not re-run the query if the result was stored.
        '''
        if query_id not in self._results:
            query_tfidf = self._query_type(self._queries[query_id])
            self._results[query_id] = query_tfidf.execute(self._index)
        return self._results[query_id]
