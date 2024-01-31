import pandas as pd
import numpy as np
from tqdm import tqdm
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('wordnet')
import utils

# Reduce words in sentence to their root form and return list of lemmatized tokens
def lemmatize(lemmatizer, sentence):
  tokens = word_tokenize(sentence)
  return [lemmatizer.lemmatize(token) for token in tokens]

def get_vad_scores(sentence, lookup, lemmatizer, negation_terms):
    arousal_scores = []
    valence_scores = []
    recognized_words = []
    recognized_count = 0

    previous_negation_index = -4
    for index, word in enumerate(lemmatize(lemmatizer, sentence)):
        if word in negation_terms:
            previous_negation_index = index
        # Bool, check if any negation terms appears within 3 index
        negate = (index - previous_negation_index) <= 3
        if word in lookup['Word'].values:
            # Get the V.Mean.Sum and A.Mean.Sum from lookup table
            row = lookup[lookup['Word'] == word]
            valence = row['V.Mean.Sum']
            arousal = row['A.Mean.Sum']
            # If any negation terms appears within 3 index, valence need to be reversed
            valence_scores.append((10 - valence) if negate else valence)
            arousal_scores.append(arousal)
            recognized_words.append(word)
            recognized_count += 1
    # Returns a tuple containing the mean arousal score, mean valence score, the list of recognized words, and the count of recognized words of the sentence
    return (np.mean(arousal_scores), np.mean(valence_scores), recognized_words, recognized_count)

# Apply each element of `data` to `wrapped_func`, which apply `data` to `func` and update progress bar
def apply_with_progress_bar(data, func, lookup, lemmatizer, negation_terms):
    with tqdm(total=len(data)) as pbar:
        def wrapped_func(x):
            pbar.update(1)
            return func(x, lookup, lemmatizer, negation_terms)
        return data.apply(wrapped_func)

def get_emotion_score(func):
    # Get data from SQL
    reddit_scraper = func
    selftext = []
    for text in reddit_scraper:
        selftext.append(text)
    data = pd.DataFrame(selftext, columns=['selftext'])

    lookup = pd.read_csv("extended-ANEW-lexicon.csv")

    lemmatizer = WordNetLemmatizer()
    negation_terms = ["no", "not", "n't","never","none","without"]

    result = apply_with_progress_bar(data['selftext'], get_vad_scores, lookup, lemmatizer, negation_terms)
    # data[['Arousal', 'Valence', 'recognized_words', 'recognized_count']] = pd.DataFrame(result.tolist(), index=data.index)
    # data[['Arousal', 'Valence','recognized_words','recognized_count']] = apply_with_progress_bar(data['selftext'], get_vad_scores, lookup, lemmatizer, negation_terms)
    data = pd.concat([data, pd.DataFrame(result.tolist(), columns=['Arousal', 'Valence', 'recognized_words', 'recognized_count'], index=data.index)], axis=1)
    data = data.dropna()
    return (data)

# Test function
# arousal = get_emotion_score(utils.get_selftext_today())["Arousal"].mean()
# print(arousal)

