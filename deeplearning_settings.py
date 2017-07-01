class GlobalSettings:
    def __init__(self):
        pass

    DICTIONARY_STOP_WORDS = "./library/stopwords.txt"
    MONGO_URI = "mongodb://localhost:27017/"
    DATABASE_DOT = "items"
    COLLECTION_PAGES = "items"
    COLLECTION_CORPUS = "corpus"
    WORKERS = 3
    WORKER_BATCH_SIZE = 50