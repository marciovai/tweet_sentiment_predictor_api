import os
import json
import flask
from flask import request, jsonify, abort
from OpenSSL import SSL
import logging
from model import *


# setup flask app
app = flask.Flask(__name__)
app.config["DEBUG"] = False

# add logging funcionality to gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/api/v1/7Aja2ByCyQ4rMBqA/predict', methods=['POST'])
def predict_tweet():
    # Called when API receives a POST request. It expects a json with
    # a dictionary of tweets, then it calls the model module to generate
    # predictios and returns it

    # Parameters:
    #    json (dict): request dict, should contain ids as keys and tweets
    # as values

    # Returns:
    #    dict (json): where the key is tweet id and value the prediction

    try:
        # get json from request
        json = request.get_json()
        
        # check if request sent an empty payload
        if json != {}:
            # get each id and tweet from request
            ids = []
            tweets = []
            for id, tweet in json.items():
                ids.append(id)
                tweets.append(tweet)

            # call model predict
            result = predict(tweets) 
            
            # generate response json
            if result == []: 
                result = empty_response(ids)
            else:
                result = prepare_response(ids, result)
        else:
            raise Exception('')

        return jsonify(result)
    except Exception as e:
        app.logger.info('Application Error while processing request')
        abort(400)

# generates response when no data is found for tweet
def empty_response(ids):
    # Called when the response from the model is empty due to no valid
    # input being passed

    # Parameters:
    #    ids (list(int)): list of passed tweet ids
    # Returns:
    #    list (id:[]): dict with passed ids as keys, empty lists for values

    # return ids for empty response
    app.logger.info("Empty response for ids: %(ids)s", {'ids': ids})
    result = {id:[] for id in ids}
    return result

# generates response for case when there is data
def prepare_response(ids, result):
  # Builds response dict when predictions are properly processed

  # Parameters:
  #    ids (list(int)): list of passed tweet ids
  #    result (list(int)): list of ints with model predictions

  # Returns:
  #   result_dict (dict): tweet ids for keys and predictions as values

    result_dict = {}
    # parse predictions to string text and append to dict
    for id, prediction in zip(ids, result):
        if prediction == 0:
            prediction = "Negative"
        if prediction == 1:
            prediction = "Positive"

        result_dict[id] = prediction

    app.logger.info("Response with data for ids: %(ids)s", {'ids': ids})
    return result_dict

# raises error if app fails
@app.errorhandler(400)
def bad_request(e):
  # Builds response when an error occurs, either with the request
  # or with the API

  # Parameters:
  #    e (Exception): Exception that occured during execution

  # Returns:
  #   json (dict): Error message and code to inform the client
    return flask.jsonify(error=400, text="Bad Request"), 400