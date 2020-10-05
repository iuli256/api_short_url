import requests
import re
import logging
import random

from app.database import Database

class Shorten():

    _url_not_exist_code = {'code': 401, 'error': 'Url doesn\'t exist'}
    _invalid_short_code = {'code': 412, 'error': 'The provided shortcode is invalid'}
    _input_validation_success = {'code': 201, 'success': 'True'}

    def _validate_url(self, url):
        try:
            rs = requests.get(url)
            if rs.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return False

    def _validate_shortcode(self, shortcode):

        if re.match(r'^[A-Za-z0-9_]+$', shortcode) and len(shortcode) == 6:
            return True

        else:
            return False

    def _shorcode_exist(self, shortcode):
        dt = Database()
        result = dt.get_shortcode(shortcode)
        if result:
            return True
        return False


    def _generate_shortcode(self):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        shortcode = ''.join(random.choice(characters) for i in range(6))
        if self._validate_shortcode(shortcode):
            if self._shorcode_exist(shortcode):
                self._generate_shortcode()
        else:
            self._generate_shortcode()
        return shortcode

    def _validate_input(self, url, shortcode):

        if not self._validate_url(url):
            return False, self._url_not_exist_code

        else:
            if shortcode and not self._validate_shortcode(shortcode):
                return False, self._invalid_short_code

        return True, self._input_validation_success

    def insert(self, url, shortcode):

        success, response = self._validate_input(url, shortcode)
        if not success:
            return success, response
        else:
            if not shortcode:
                shortcode = self._generate_shortcode()
            if self._shorcode_exist(shortcode):
                return False, { 'code': 409, 'error': 'Shorcode {} already in use'.format(shortcode)}
            else:
                dt = Database()
                success = dt.insert_shortcode(shortcode, url)
                if not success:
                    logging.error('Shortcode {} and url not inserted'.format(shortcode, url))
                    return False, {'error': 'something very bad had happened', 'code': 455}

        return True, {'shortcode': shortcode, 'code': 201}