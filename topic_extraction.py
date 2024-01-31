
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer, util
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired
from bertopic.representation import MaximalMarginalRelevance
from sentence_transformers import SentenceTransformer
import numpy as np
import re

from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN
from sqlalchemy import create_engine
import pandas as pd
import utils

def topic(func):
  reddit_scraper = func
  selftext = []
  for text in reddit_scraper:
      selftext.append(text)
  docus = pd.DataFrame(selftext, columns=['selftext'])

  sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

  representation_model = MaximalMarginalRelevance(diversity=0.1)

  umap_model = UMAP(n_neighbors=5, n_components=3, min_dist=0.0, metric='cosine')

  hdbscan_model = HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

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
  # print(topic_model.get_topic_info())
  # print(topic_model.visualize_barchart(top_n_topics=10))
  topic_labels = topic_model.generate_topic_labels()

  topic_info = topic_model.get_document_info(docus['selftext'])
  topic_appended = pd.concat([topic_info,docus],axis=1)
  topic_appended = topic_appended.drop(['Document'], axis=1, inplace=True)
  return topic_appended
  # print(topic_appended.head())
  # topic_appended.to_csv("topic-output.csv")