from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm
from hdbscan import HDBSCAN
from sqlalchemy import create_engine
import pandas as pd
from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm
import utils

def SuiBERT(func):
    suibert = BertForSequenceClassification.from_pretrained('SuiBERT_model', num_labels=2)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', model_max_length=512)
    nlp = pipeline("text-classification", model=suibert, tokenizer=tokenizer, device=-1, truncation=True)  # Use device=-1 for CPU

    reddit_scraper = func
    selftext = []
    for text in reddit_scraper:
        selftext.append(text)
    docus = pd.DataFrame(selftext, columns=['selftext'])

    selftext_list = docus['selftext'].tolist()
    labels = []
    scores = []
    for out in tqdm(nlp(selftext_list)):
        labels.append(out['label'])
        scores.append(out['score'])

    prediction = pd.DataFrame({'selftext': selftext_list, 'Prediction_label': labels, 'Prediction_score': scores})
    return prediction

# Test model
# print(SuiBERT(utils.get_selftext_today()).head())


# Test model

# text = "The sun is shining, and it's a beautiful day outside!"
# text2 = "I'm really sorry to hear that you're feeling this way, but I can't provide the help that you need. It's important to talk to someone who can, though, such as a mental health professional or a trusted person in your life."
# text3 = "Coming soon: add-ons and plug-ins for the community, by the community! Browse redditor-made post units, bots, mod tools and more! Sign up to be the first to know when our Community Directory is live."
# text4 = "i have been in psychosis for around 1 year now and it was really bad at the beginning but i have been better now. but recently it’s been getting worse again. before i would just see cats and eyes on the wall and have minor violent auditory hallucinations. now im getting terrible hallucinations like seeing a woman with no eyelids in my house and getting terrifying auditory hallucinations that keep me awake at night. those are nothing compared to what i saw in the backyard. it started off with a man on his knees in the grass area then another man popped up behind him then grabbed his throat and ripped it. i called the police but there was nothing back there, it felt so real. this happened a few days ago and still terrifies me it hasn’t left my mind"
# result = nlp(text4)
# label = result[0]['label']
# score = result[0]['score']
# print("Label:", label)
# print("Score:", score)




