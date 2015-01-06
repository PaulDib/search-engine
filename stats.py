from index.clients.statistics import StatsGenerator

generator = StatsGenerator()
generator.set_index_path('data/cacm.all', 'data/common_words')
generator.set_query_path('data/query.text', 'data/qrels.text')
generator.set_output_folder('images')
generator.set_iterations(100)
generator.compute_statistics()




