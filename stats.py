from index.core.index import Index
from index.core.index_config import IndexConfig
from index.core.vectorial_query import VectorialQueryTfIdf, VectorialQueryNormCount
from math import ceil
from pylab import *


def read_queries(file_path):
    queries = {}
    query_id = 0
    with open(file_path) as file_ptr:
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


def read_expected_results(file_path):
    expected = {}
    with open(file_path) as file_ptr:
        for line in file_ptr:
            splitted = line.split(" ")
            query_id = int(splitted[0])
            expected_doc = int(splitted[1])
            if query_id in expected:
                expected[query_id].append(expected_doc)
            else:
                expected[query_id] = [expected_doc]
    return expected

def compute_recall_and_precision(queries, expected, index, query_type, chart_title, output_path, step=1):
    average_prec_list = []
    average_recall_list = []
    results = {}

    for percentage in range(1, 100, 1):
        average_prec = 0
        average_recall = 0
        for (query_id, query_text) in queries.items():
            pertinent = expected[query_id] if query_id in expected else []
            pertinent_len = len(pertinent)

            if query_id not in results:
                query_tfidf = query_type(query_text)
                query_results = query_tfidf.execute(index)
                results[query_id] = query_results
            else:
                query_results = results[query_id]
            
            tfidf_len = len(query_results)

            top = math.ceil(tfidf_len*percentage/100)
            query_results = query_results[0:top]
            tfidf_len = top
            
            tfidf_found = len([k for k in pertinent if k in [x for (x, y) in query_results]])
            tfidf_recall = tfidf_found / pertinent_len if pertinent_len > 0 else 1.0
            tfidf_prec = tfidf_found / tfidf_len
            
            average_prec = average_prec + tfidf_prec
            average_recall = average_recall + tfidf_recall
        average_prec = average_prec / len(queries)
        average_recall = average_recall / len(queries)
        average_prec_list.append(average_prec)
        average_recall_list.append(average_recall)

    plot(average_recall_list, average_prec_list)

    xlabel('recall')
    ylabel('precision')
    title(chart_title)
    grid(True)
    savefig("images/" + output_path)


print('Indexing...')
config = IndexConfig('data/common_words')
index = Index('data/cacm.all', config)

queries = read_queries('data/query.text')
expected = read_expected_results('data/qrels.text')

print('Running queries...')
compute_recall_and_precision(queries, expected, index,
                             VectorialQueryTfIdf, 'tfidf', 'tfidf.png')
compute_recall_and_precision(queries, expected, index,
                              VectorialQueryNormCount, 'normalized_count',
                              'normalized_count.png')






# query_norm_count = VectorialQueryNormCount(query_text)
# results_norm_count[query_id] = query_norm_count.execute(index)
# norm_count_len = len(results_norm_count[query_id])
# norm_count_found = len([k for k in pertinent if k in [x for (x, y) in results_norm_count[query_id]]])
# norm_count_recall = norm_count_found / pertinent_len if pertinent_len > 0 else 1.0
# norm_count_prec = norm_count_found / norm_count_len

# print('q{0} tfidf r:{1:.3f} p:{2:.3f} - n_cnt r:{3:.3f} p:{4:.3f}'.format(
#     query_id, tfidf_recall, tfidf_prec, norm_count_recall, norm_count_prec))


    