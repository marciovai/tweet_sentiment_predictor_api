from .api import app

# this file is used to pass the app context to WSGI Gunicorn

if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(host='0.0.0.0', debug=False, ssl_context=context, threaded=True)