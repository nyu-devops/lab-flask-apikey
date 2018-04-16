# lab-flask-apikey
This repository will show you how to implement a simple API key based security using Python / Flask

## Key functions

Here are the key functions that make it all work:

## requires_apikey()

The work is done in a decorator function `@requires_apikey` which can be placed before any route that you want to secure by requireing an api key be passed in the headers.

```Python
def requires_apikey(f):
    """ Decorator function to require API Key """
    @wraps(f)
    def decorated(*args, **kwargs):
        """ Decorator function that does the checking """
        if check_auth():
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated

```

## check_auth()

This the code that looks for the existence of the API key in the header and checks if it matches the API key in the environment. You can make this as elaborate as you'd like placing the API keys in a database and doing a lookup to determine if it's a key that you recognise and is valid.

```Python
def check_auth():
    """ Checks the environment that the API_KEY has been set """
    if app.config['API_KEY']:
        return app.config['API_KEY'] == request.headers.get('X-Api-Key')
    return False
```

## not_authorized(()

This is actually an error handler for the `401` error. Since this is a microservice that communicates via `json` we want to be sure to send back a `json` formatted error message to the cloent and not `html`.

```Python
@app.errorhandler(401)
def not_authorized(e):
    """ Respose sent back when not autorized """
    return jsonify(status=401, error='Not Authorized',
                   message='You are authorized to access the URL requested.'), 401
```

With these three functions you can protect any API call by requiring that a secret API key be present in the header of the call.
