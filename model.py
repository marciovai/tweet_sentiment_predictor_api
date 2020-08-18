import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import log_loss, accuracy_score
import inspect
import joblib
import re


def load_artifact(item):
  # loads the vocabulary dict or model based on item parameter
  if item == 'vocab_dict':
    return joblib.load('./artifacts/word_vocab_dict_v1.joblib')
  if item == 'model':
    return joblib.load('./artifacts/tweet_sentiment_logistic_v1.joblib')

def process_tweet(tweet, stop_words):

  # remove URLs from the tweet
  tweet = re.sub(r"http\S+", "", tweet)

  # remove punctuation
  tweet = re.sub(r'[^\w\s]','', tweet)

  # tokenize tweet (transform from string into list of word)
  tweet = word_tokenize(tweet) 

  # remove stop words using the set() imported from NTLK
  tweet = [word for word in tweet if word not in stop_words]

  # apply stemming on the tweet
  ps = PorterStemmer() 
  tweet = [ps.stem(word) for word in tweet]

  # lowercase all words in the tweet
  tweet = [word.lower() for word in tweet]

  return tweet

def get_tweet_word_frequencies(word_vocab_dict, tweet_text):
  # initialize total frequency variables
  pos_total_freq = 0
  neg_total_freq = 0

  for word in tweet_text:
    # for each word in the tweet, get its positive and negative frequency
    neg_freq = word_vocab_dict.get((word, 0), 0)
    pos_freq = word_vocab_dict.get((word, 1), 0)

    # sum positive and negative frequencies of current word to running total
    neg_total_freq+=neg_freq
    pos_total_freq+=pos_freq

  return [neg_total_freq, pos_total_freq]

def preprocess(predict_data):
  # prepare data

  # load list of stopwords from NLTK
  nltk.download('stopwords', quiet=True)
  nltk.download('punkt', quiet=True)

  # save stopwords in a Python set
  stop_words = set(stopwords.words('english'))
  if not word_vocab_dict:
    # load vocabulary dict to get word count features
    word_vocab_dict = load_artifact('vocab_dict')

  # list to store processed tweets
  predict_tweets_list = []

  # iterate over each row, call process(tweet) and save it on predict_tweets_list
  for tweet in predict_data:
    tweet = process_tweet(tweet, stop_words)
    predict_tweets_list.append(tweet)

  # call get_tweet_word_frequencies() and store results in a DataFrame
  predict_ar = np.array([]) 
  for tweet in predict_tweets_list:
    tweet_features = get_tweet_word_frequencies(word_vocab_dict, tweet)
    predict_ar = np.concatenate((predict_ar, np.array(tweet_features)))

  # making sure our data is shape (tweet_features, tweets)
  predict_ar = predict_ar.reshape(len(predict_tweets_list), 2)

  return predict_ar

def predict(predict_data):
  import pdb;pdb.set_trace()
  # preprocess input data
  predict_data_prep = preprocess(predict_data)

  if not model:
    # load model
    model = load_artifact('model')

  # call model predict
  prediction = model.predict(predict_data_prep)

  # if prediction >= 0.5, label=1 else, label=0
  prediction = (prediction>= 0.5).astype(int)

  # return prediction on a 1D array E(0, 1)
  return prediction.ravel()