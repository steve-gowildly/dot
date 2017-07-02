import multiprocessing
import sys
import time
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from deeplearning_settings import GlobalSettings

"""
Loads the list of stop words to ignore in the provided page content.
"""
def load_stopwords():
    stopwords = {}
    with open(GlobalSettings.DICTIONARY_STOP_WORDS, 'rU') as f:
        for line in f:
            stopwords[line.strip()] = 1

    return stopwords


"""
The worker that takes each page and splits the page content into sentences, removes stopwords,
extracts parts-of-speech tags for all the remaining tokens, and stores each processed page into the corpus db.
"""
def worker(identifier, skip, count):
    done = 0
    start = time.time()

    # Connect to the pages and corpus databases
    stopwords = load_stopwords()
    pages_db = MongoClient(GlobalSettings.MONGO_URI)[GlobalSettings.DATABASE_DOT][GlobalSettings.COLLECTION_PAGES]
    corpus_db = MongoClient(GlobalSettings.MONGO_URI)[GlobalSettings.DATABASE_DOT][GlobalSettings.COLLECTION_CORPUS]

    # Create an instance of the lemmatizer to process the nouns
    lem = WordNetLemmatizer()

    # Set the batch size for this worker
    batch_size = GlobalSettings.WORKER_BATCH_SIZE
    for batch in range(0, count, batch_size):
        # Get the correct cursor position in the pages db and grab the batch of pages
        pages_cursor = pages_db.find().skip(skip + batch).limit(batch_size)
        # Go through each of the pages and clean/extract the words
        for page in pages_cursor:
            words = []
            nouns = []

            # Check to make sure the page does have cleaned text to analyze. Otherwise we ignore it.
            if "cleaned_text" in page:
                # Check to see if this key already exists in the corpus
                document = corpus_db.find_one({"_id": page["url"]})

                # If there isn't a document, we process this page as we need to add it
                if document is None:
                    # Tokenize the content into sentences and put everything into lowercase
                    sentences = nltk.sent_tokenize(page["cleaned_text"].lower())

                    # Go through each sentence and clean/extract words
                    for sentence in sentences:
                        # Tokenize the sentence into words and remove those in the stopwords list
                        tokens = nltk.word_tokenize(sentence)
                        text = [word for word in tokens if word not in stopwords]
                        # Tag each word with it's type (e.g. noun, verb, etc)
                        tagged_text = nltk.pos_tag(text)

                        # Create the list of words and positions
                        for word, tag in tagged_text:
                            words.append({"word": word, "pos": tag})

                    # Now that we have the words, we do another pass to get those that are nouns
                    words = [word for word in words if word["pos"] in ["NN", "NNS"]]

                    # Lemmatize the nouns so we have a clean set
                    for word in words:
                        nouns.append(lem.lemmatize(word["word"]))

                    # Once we've processed the sentences in the content into words, we push this back into the corpus db
                    corpus_db.insert({
                        "_id": page["url"],
                        "url": page["url"],
                        "text": page["cleaned_text"],
                        "words": nouns
                    })

            # Check to see if the worker is done and log appropriately
            done += 1
            if done % 100 == 0:
                end = time.time()
                print 'Worker' + str(identifier) + ': Done ' + str(done) + ' out of ' + str(count) + ' in ' + (
                    "%.2f" % (end - start)) + ' sec ~ ' + ("%.2f" % (done / (end - start))) + '/sec'
                sys.stdout.flush()


"""
The entry point for kicking off separate worker tasks to process the page content.
"""
def main():
    # Download the necessary information needed for gensim
    # nltk.download()

    # Get the count of pages stored in MongoDb
    pages_db = MongoClient(GlobalSettings.MONGO_URI)[GlobalSettings.DATABASE_DOT][GlobalSettings.COLLECTION_PAGES]
    pages_cursor = pages_db.find()
    count = pages_cursor.count()

    # Create workers to go through the pages in separate batches
    workers = GlobalSettings.WORKERS
    batch = count / workers
    left = count % workers

    # Kick off each worker until all batches have completed processing
    jobs = []
    for i in range(workers):
        size = count / workers
        if i == (workers - 1):
            size += left
        p = multiprocessing.Process(target=worker, args=((i + 1), i * batch, size))
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()
        print '%s.exitcode = %s' % (j.name, j.exitcode)


if __name__ == '__main__':
    main()
