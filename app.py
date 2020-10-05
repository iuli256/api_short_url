import logging

from app.shortcode import Shortcode
from app.shorten import Shorten
from flask import Flask, Response, jsonify, request,redirect


app = Flask(__name__)


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed. Please check the documentation'}), 405


@app.route("/", methods=["GET"])
def index() -> Response:
    response = {"status": "ok"}
    return response


@app.route("/shorten", methods=["POST"])
def shorten() -> Response:
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    try:
        response = {}
        url = None
        shortcode = None

        if not request.form.get('url'):
            response['error'] = 'Url not present'
            return response, 400
        else:
            url = request.form.get('url')

        if request.form.get('shortcode'):
            shortcode = request.form.get('shortcode')
        short = Shorten()
        success, response = short.insert(url, shortcode)
        if success:
            return {'shortcode': response['shortcode']}, response['code']
        else:
            return {'error': response['error']}, response['code']
    except Exception as error:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(error).__name__, error.args)
        logging.error("Error getting shortcode - {0}".format(message))

    return {'error': 'something wrong happened'}, 500


@app.route("/<shortcode>", methods=["GET"])
def shortcode(shortcode) -> Response:
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    try:
        sc = Shortcode()
        response, code = sc.get_url(shortcode)
        if code == 404:
            return response, code
        else:
            return redirect(response['url'], code=302)
    except Exception as error:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(error).__name__, error.args)
        logging.error("Error getting shortcode - {0}".format(message))

    return {'error': 'something wrong happened'}, 500


@app.route("/<shortcode>/stats", methods=["GET"])
def shortcode_stats(shortcode) -> Response:
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    try:
        code = 200
        sc = Shortcode()
        response, code = sc.get_stats(shortcode)
        if code == 404:
            return response, code
        else:
            return response, code
    except Exception as error:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(error).__name__, error.args)
        logging.error("Error getting shortcode - {0}".format(message))

    return {'error': 'something wrong happened'}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
