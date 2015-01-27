# search-engine
Information Retrieval Course project.
Search engine implementing several models on a small collection of documents.

###Python version
The project uses Python 3. It was tested with version `3.4.2`.

##Dependencies
The project uses several external packages:
- nltk
- pyparsing
- matplotlib
- pympler


You can retrieve them using `pip install --user package-name`. (Make sure you're running `pip` for Python 3)

`Matplotlib` is likely to cause troubles installing via `pip`, you may want to refer to the [Matplotlib installing FAQ](http://matplotlib.org/faq/installing_faq.html).

##Tests
The tests can be run using `nosetests3`. Simply type `nosetests3` at the root of the repository.

##Running
###Evaluation summary
To run an evaluation summary on the index (creating the index and running different types of queries), use the `stats.py` file. You can change evaluation parameters in the `stats.py` script before running it with:

```bash
python stats.py
```

###REPL client
To run an interactive console that lets you run queries or export the index, use the `repl.py` script. Simply run:

```bash
python repl.py
```

###Indexing INEX
***This operation WILL take a long time (more than one hour, depending on the number of processes) and will use a huge amount of RAM (2.70 Go).***

You must download the INEX 2007 collection and extract the archived files into a single folder (this folder must contain all the `.xml` documents). Edit the `inex.py` script to add the correct path to the corpus folder and run:

```bash
python inex.py
```
