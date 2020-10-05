from app.database import Database
import logging

class Shortcode():

    def get_url(self, shortcode):
        response = {}
        code = 404
        dt = Database()

        result = dt.get_shortcode(shortcode)
        if result:
            upd = dt.update_result_count(shortcode, result[3] + 1)
            if not upd:
                logging.error('Shortcode {} not updated'.format(shortcode))
            response['url'] = result[5]
            code = 302
        else:
            response['error'] = 'Shortcode not found'
        return response, code

    def get_stats(self, shortcode):
        response = {}
        code = 404
        dt = Database()

        result = dt.get_shortcode(shortcode)
        if result:
            response['created'] = result[1].isoformat()
            response['lastRedirect'] = result[2].isoformat() if result[2] else None
            response['redirectCount'] = result[3]
            code = 302
        else:
            response['error'] = 'Shortcode not found'
        return response, code
