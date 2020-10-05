import requests
import responses
import pytest
from unittest import mock

from app.shorten import Shorten
from app.database import Database

@responses.activate
def test_validate_url_error():
    responses.add(
        responses.GET,
        "http://api.zippopotam.us/us/90210",
        json={"error": "No data exists for US zip code 90210"},
        status=404
    )
    sh = Shorten()
    resp = sh._validate_url('http://api.zippopotam.us/us/90210')
    assert resp == False


@responses.activate
def test_validate_url_succes():
    responses.add(
        responses.GET,
        "http://api.zippopotam.us/us/90210",
        json={"success": "zip code 90210"},
        status=200
    )
    sh = Shorten()
    resp = sh._validate_url('http://api.zippopotam.us/us/90210')
    assert resp == True


def test_validate_shortcode_success():

    shortcode = 'test12'
    sh = Shorten()
    response = sh._validate_shortcode(shortcode)

    assert response == True


def test_validate_shortcode_failure():
    shortcode = 'test'
    sh = Shorten()
    response = sh._validate_shortcode(shortcode)

    assert response == False


def test_shorcode_exist_false():
    with mock.patch("app.database.Database.get_shortcode") as complex_function_mock:
        complex_function_mock.return_value = False
        sh = Shorten()
        re = sh._shorcode_exist('ss')
        assert not re



def test_shorcode_exist_success():
    with mock.patch("app.database.Database.get_shortcode") as complex_function_mock:
        complex_function_mock.return_value = True
        sh = Shorten()
        re = sh._shorcode_exist('ss')
        assert re

def test_validate_input_success():
    with mock.patch("app.shorten.Shorten._validate_url") as mocking:
        mocking.return_value = True
        sh = Shorten()
        re = sh._validate_input('url', 'test12')
        assert re == (True, {'code': 201, 'success': 'True'})


def test_validate_input_error_url():
    with mock.patch("app.shorten.Shorten._validate_url") as mocking:
        mocking.return_value = False
        sh = Shorten()
        re = sh._validate_input('url', 'test12')
        assert re == (False, {'code': 401, 'error': 'Url doesn\'t exist'})


def test_validate_input_error_shorten():
    with mock.patch("app.shorten.Shorten._validate_url") as mocking:
        mocking.return_value = True
        sh = Shorten()
        re = sh._validate_input('url', 'test')
        assert re == (False, {'code': 412, 'error': 'The provided shortcode is invalid'})


def test_insert_error_validation():
    with mock.patch("app.shorten.Shorten._validate_input") as mocking:
        mocking.return_value = (False, {'code': 412, 'error': 'The provided shortcode is invalid'})
        sh = Shorten()
        re = sh._validate_input('url', 'test')
        assert re == (False, {'code': 412, 'error': 'The provided shortcode is invalid'})
