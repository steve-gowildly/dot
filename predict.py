import logging
import nltk
from gensim.models import LdaModel
from gensim import corpora
from nltk.stem.wordnet import WordNetLemmatizer
from deeplearning_settings import GlobalSettings


class Predict():
    def __init__(self):
        dictionary_path = "models/dictionary.dict"
        lda_model_path = "models/lda_model_50_topics.lda"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def load_stopwords(self):
        stopwords = {}
        with open(GlobalSettings.DICTIONARY_STOP_WORDS, 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        return stopwords

    def extract_lemmatized_nouns(self, new_review):
        stopwords = self.load_stopwords()
        words = []

        sentences = nltk.sent_tokenize(new_review.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        lem = WordNetLemmatizer()
        nouns = []
        for word in words:
            if word["pos"] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word["word"]))

        return nouns

    def run(self, new_review):
        nouns = self.extract_lemmatized_nouns(new_review)
        new_review_bow = self.dictionary.doc2bow(nouns)
        new_review_lda = self.lda[new_review_bow]

        print new_review_lda


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    topic_content = "President Donald Trump called out the nearly 30 states expressing concerns about the " \
                    "legality of his administration's efforts to investigate voter fraud, asking what the " \
                    "states might be hiding in a tweet Saturday morning. \"Numerous states are refusing to " \
                    "give information to the very distinguished VOTER FRAUD PANEL. What are they trying to hide,\" " \
                    "Trump wrote."

    predict = Predict()
    predict.run(topic_content)


if __name__ == '__main__':
    main()


