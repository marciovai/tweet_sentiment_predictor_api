import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.linear_model import LinearRegression
import joblib
import re


def load_artifact(item):
	"""
	Receives a string as input indicating which artifact object
	to load and returns it to the calling method

	Parameters:
	item (str): The item to be loaded and returned

	Returns:
	model (LogisticRegression): LogisticRegression model
	or word_vocab_dict (dict): dict with corpus word frequencies
	"""
	# loads the vocabulary dict or model based on item parameter
	if item == "vocab_dict":
		return joblib.load("./artifacts/word_vocab_dict_v1.joblib")
	if item == "model":
		return joblib.load("./artifacts/tweet_sentiment_logistic_v1.joblib")


def process_tweet(tweet, stop_words):
	"""
	Receives a raw tweet, a list of stop words and performs a series of 
	preprocessing in the data.

	Parameters:
	tweet (str): Tweet raw string body
	stop_words (set(str)): set containing English stopwords from NLTK

	Returns:
	tweet (str): Fully preprocessed tweet
	"""
	# remove URLs from the tweet
	tweet = re.sub(r"http\S+", "", tweet)

	# remove punctuation
	tweet = re.sub(r"[^\w\s]", "", tweet)

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
	"""
	Receives a count of sentiment frequencies for each word in the corpus and a 
	tweet then it computes the word frequencies to it

	Parameters:
	word_vocab_dict (dict): contains words and sentiment as keys and 
	total count in the corpus as value
	tweet_text (str): preprocessed tweet to generate word frequencies

	Returns:
	list(int): two integers, for positive and negative word frequencies
	in the tweet
	"""
	# initialize total frequency variables
	pos_total_freq = 0
	neg_total_freq = 0

	for word in tweet_text:
		# for each word in the tweet, get its positive and negative frequency
		neg_freq = word_vocab_dict.get((word, 0), 0)
		pos_freq = word_vocab_dict.get((word, 1), 0)

		# sum positive and negative frequencies of current word to running total
		neg_total_freq += neg_freq
		pos_total_freq += pos_freq

	return [neg_total_freq, pos_total_freq]


def preprocess(predict_data):
	"""
	Given a list of raw tweets, performs preprocessing to it
	before it can be fed to the model as input.

	Parameters:
	predict_data (list(str)): list of raw tweets text

	Returns:
	list (list(int)): preprocessed tweets
	"""

	# load list of stopwords from NLTK
	nltk.download("stopwords", quiet=True)
	nltk.download("punkt", quiet=True)

	# save stopwords in a Python set
	stop_words = set(stopwords.words("english"))

	# load vocabulary dict to get word count features
	word_vocab_dict = load_artifact("vocab_dict")

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

	# making sure data is of shape (tweet_features, tweets)
	predict_ar = predict_ar.reshape(len(predict_tweets_list), 2)

	return predict_ar


def predict(predict_data):
	"""
	Main module execution method, once called by the api to make predictions,
	it calls all other methods in the module and returns the prediction

	Parameters:
	predict_data (list(str)): list of raw tweets text

	Returns:
	list (int): model prediction as integers in (0, 1)
	"""
	# preprocess input data
	predict_data_prep = preprocess(predict_data)

	# load model
	model = load_artifact("model")

	# call model predict
	prediction = model.predict(predict_data_prep)

	# if prediction >= 0.5, label=1 else, label=0
	prediction = (prediction >= 0.5).astype(int)

	# return prediction on a 1D array E(0, 1)
	return prediction.ravel()
