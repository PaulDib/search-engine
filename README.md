# search-engine
Information Retrieval Course project.
Search engine implementing several models on a small collection of documents.

###Python version
The project uses Python 3. It was tested with version `3.4.2`.

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
***This is a work in progress. Running `inex.py` on the whole INEX collection will certainly fail in a spectacular manner. You've been warned.***

You must download the INEX 2007 collection and extract the archived files into a single folder (this folder must contain all the `.xml` documents). Edit the `inex.py` script to add the correct path to the corpus folder and run:

```bash
python inex.py
```
