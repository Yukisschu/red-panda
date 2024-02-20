import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import MaximalMarginalRelevance
from sentence_transformers import SentenceTransformer
import utils


def topic(func):
    reddit_collector = func
    selftext = []
    for text in reddit_collector:
        selftext.append(text)
    docus = pd.DataFrame(selftext, columns=['selftext'])

    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

    representation_model = MaximalMarginalRelevance(diversity=0.05)

    umap_model = UMAP(n_neighbors=3, n_components=3, min_dist=0.0, metric='cosine')

    hdbscan_model = HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom',
                            prediction_data=True)

    vectorizer_model = CountVectorizer(stop_words="english")

    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

    topic_model = BERTopic(
        representation_model=representation_model,
        embedding_model=sentence_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=ctfidf_model,
        calculate_probabilities=True,
        verbose=True
    )
    topics, probabilities = topic_model.fit_transform(docus['selftext'])
    topic_info = topic_model.get_document_info(docus['selftext'])
    print(topic_info.head())
    topic_appended = pd.concat([topic_info, docus], axis=1)
    topic_appended = topic_appended.drop(['Document'], axis=1)
    topic_appended.to_csv('topic.csv')
    return topic_appended


topic = topic(utils.get_selftext_today())

