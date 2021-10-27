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
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route("/api/v1/7Aja2ByCyQ4rMBqA/predict", methods=["POST"])
def predict_tweet():
    """
    Called when API receives a POST request. It expects a json with
    dictionary of tweets, then it calls the model module to generate
    predictioNs and returns it

    Parameters:
    json (dict): request dict, should contain ids as keys and tweets
    as values

    Returns:
    dict (json): key is tweet id and value the prediction
    """

    try:
        # get request json
        json = request.get_json()

        # check if payload is empty
        if json != {}:
            # get each id and tweet from request
            ids = []
            tweets = []
            for id, tweet in json.items():
                ids.append(id)
                tweets.append(tweet)

            # get predictions
            result = predict(tweets)

            # generate response json
            if result == []:
                result = empty_response(ids)
            else:
                result = prepare_response(ids, result)
        else:
            raise RuntimeError("Error while processing response")

        return jsonify(result)
    except Exception as e:
        app.logger.info("Application Error while processing request")
        abort(400)


def empty_response(ids):
    """
    Called when the response from the model is empty due to no valid
    input being passed

    Parameters:
        ids (list(int)): list of given tweet ids
    Returns:
        list (id:[]): dict with given ids as keys, empty lists for values
    """
    # return ids for empty response
    app.logger.info("Empty response for ids: %(ids)s", {"ids": ids})
    result = {id: [] for id in ids}
    return result


def prepare_response(ids, result):
    """
    Builds response dict when predictions are correctly processed

    Parameters:
        ids (list(int)): list of passed tweet ids
        result (list(int)): list of ints with model predictions

    Returns:
        result_dict (dict): tweet ids for keys and predictions as values
    """
    result_dict = {}
    # parse predictions to string text and append to dict
    for id, prediction in zip(ids, result):
        if prediction == 0:
            prediction = "Negative"
        if prediction == 1:
            prediction = "Positive"

        result_dict[id] = prediction

    app.logger.info("Response with data for ids: %(ids)s", {"ids": ids})
    return result_dict


# raises error if app fails
@app.errorhandler(400)
def bad_request(e):
    """
    Builds response when an error is raised.

    Parameters:
        e (Exception): Exception that occured during execution

    Returns:
        json (dict): Error message and code to inform the client
    """        
    return flask.jsonify(error=400, text="Bad Request"), 400
