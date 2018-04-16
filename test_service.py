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
# Test cases can be run with any of the following:
# coverage report -m --include=service.py
# nosetests -v --rednose --with-coverage --cover-package=service

import unittest
import service

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetServer(unittest.TestCase):

    def setUp(self):
        service.app.debug = True
        self.app = service.app.test_client()
        api_key = service.generate_apikey()
        service.app.config['API_KEY'] = api_key
        self.headers = {'X-Api-Key': api_key}

    def test_index(self):
        """ Test the home page which is not protected """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Example Flask API Key Demo' in resp.data)

    def test_not_authorized(self):
        """ Test call that is not autorized """
        resp = self.app.get('/pets')
        self.assertEqual(resp.status_code, 401)

    def test_get_pet_list(self):
        """ Test call with autorization """
        resp = self.app.get('/pets', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) > 0)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
