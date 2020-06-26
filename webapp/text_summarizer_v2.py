from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk.tokenize import sent_tokenize, word_tokenize
import networkx as nx
import numpy as np

stop_words = stopwords.words('english')


def read_article(stuff):
    article = sent_tokenize(stuff)
    sentences = []

    for sentence in article:
        sentence = sentence[:-1]
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))

    return sentences


def sentence_similarity(sent_1, sent_2, stop_words=stop_words):
    sent_1 = [w.lower() for w in sent_1]
    sent_2 = [w.lower() for w in sent_2]
    all_words = list(set(sent_1+sent_2))
    vector_1 = [0]*len(all_words)
    vector_2 = [0] * len(all_words)

    for w in sent_1:
        if w not in stop_words:
            vector_1[all_words.index(w)] += 1

    for w in sent_2:
        if w not in stop_words:
            vector_2[all_words.index(w)] += 1

    cos_distance = 1-cosine_distance(vector_1, vector_2)
    return cos_distance


def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for index_1 in range(len(sentences)):
        for index_2 in range(len(sentences)):
            if index_1 == index_2:
                continue
            similarity_matrix[index_1][index_2] = sentence_similarity(
                sentences[index_1], sentences[index_2], stop_words)
    return similarity_matrix


def generate_summary(stuff, num_of_sentences=5, stop_words=stop_words):
    summary = []
    verification_sentences = []
    final_summary = []
    sentences = read_article(stuff)
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentences = sorted(
        ((scores[i], n) for i, n in enumerate(sentences)), reverse=True)

    for i in range(num_of_sentences):
        summary.append(" ".join(ranked_sentences[i][1]))
    for i in range(len(sentences)):
        verification_sentences.append(" ".join(sentences[i]))
    for sent in verification_sentences:
        if sent in summary:
            final_summary.append(sent)
    summarization = ". ".join(final_summary)
    return summarization
