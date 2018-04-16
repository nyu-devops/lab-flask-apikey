"""
 Copyright 2016, 2018 John J. Rofrano. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import os
import uuid
from functools import wraps
from flask import Flask, request, jsonify, abort, url_for

# Get global variables from the environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = int(os.getenv('PORT', '5000'))
HOST = str(os.getenv('VCAP_APP_HOST', '0.0.0.0'))

app = Flask(__name__)
app.config['API_KEY'] = os.getenv('API_KEY', None)

######################################################################
# HTTP Error Handlers
######################################################################
@app.errorhandler(401)
def not_authorized(e):
    """ Respose sent back when not autorized """
    return jsonify(status=401, error='Not Authorized',
                   message='You are authorized to access the URL requested.'), 401

######################################################################
# Check Auth: Add your autorization code here
######################################################################
def check_auth():
    """ Checks the environment that the API_KEY has been set """
    if app.config['API_KEY']:
        return app.config['API_KEY'] == request.headers.get('X-Api-Key')
    return False

######################################################################
# Requires API Key: Decorator function to add secuity to any call
######################################################################
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

######################################################################
# GET /
######################################################################
@app.route('/')
def index():
    """ Home page which is not protected """
    return jsonify(message='Example Flask API Key Demo',
                   url=url_for('get_pets', _external=True),
                   version='1.0'), 200

######################################################################
# GET /pets
######################################################################
@app.route('/pets', methods=['GET'])
@requires_apikey
def get_pets():
    """ Call to get Pets which is protected by API key """
    pets = [{'name':'fido', 'category':'dog'},
            {'name':'kitty', 'category':'cat'}]
    return jsonify(pets), 200


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex

######################################################################
#  M A I N   P R O G R A M
######################################################################
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
