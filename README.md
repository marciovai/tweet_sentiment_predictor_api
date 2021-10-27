# tweet_sentiment_predictor_api
Template for deploying a ML model for predicting Sentiment of a tweet from Twitter. An API will be available to get live predictions from the model.

To BUILD the container:

```bash
docker build -t model_api:latest . 
```

To RUN, the Dockerfile assumes the project files are on the root folder:
```bash
docker run -it -v /path/to/model_api/:/external_lib/ -p 5000:5000 model_api sh -c 'cd external_lib && make api-start' 
```

The API will be started on port 5000 and listen for connections.