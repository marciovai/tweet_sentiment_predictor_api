# tweet_sentiment_predictor_api
Template to make deploying Machine Learning algorithms in production easier and allow it to later be consumed via an API.

This particular example is developed using Twitter Sentiment Prediction.

Use the following command to BUILD the container:

```bash
docker build -t model_api:latest . 
```

Once built, the Dockerfile assumes the project files are on the root folder. To RUN the API use:
```bash
docker run -it -v /path/to/model_api/:/external_lib/ -p 5000:5000 model_api sh -c 'cd external_lib && make api-start' 
```

It will start the API on port 5000 to listen to connections.
