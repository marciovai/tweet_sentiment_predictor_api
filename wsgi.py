from api import app

# Passes the app context to WSGI Gunicorn when running the API

if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(host='0.0.0.0', debug=False, ssl_context=context, threaded=True)