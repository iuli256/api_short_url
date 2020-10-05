from configparser import ConfigParser
import psycopg2

class Database():
    _schema = None

    def _get_config(self, filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                if param[0] == 'schema':
                    self._schema = param[1]
                else:
                    db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def _connect(self):
        conn = None
        try:
            params = self._get_config()
            conn = psycopg2.connect(**params)
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_shortcode(self, shortcode):
        conn = self._connect()

        cursor = conn.cursor()
        cursor.execute("set search_path to %(schema)s; "
                    " select sc.id, sc.created, sc.last_redirect, sc.redirect_count, sc.short_code, sc.url "
                    " from short_codes as sc where sc.short_code = %(shortcode)s ;",
                    {'schema': self._schema, 'shortcode': shortcode})
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return False

        return result

    def update_result_count(self, shortcode, redirectcount):
        conn = self._connect()
        cursor = conn.cursor()
        print(" === start insert ===")
        cursor.execute("set search_path to %(schema)s; "
                        " UPDATE short_codes "
                        " SET "
                        " last_redirect=now(), redirect_count=%(redirectcount)s"
                        " where short_code=%(shortcode)s; ",
                       {'schema': self._schema, 'shortcode': shortcode, 'redirectcount': redirectcount})
        conn.commit()
        count = cursor.rowcount
        if count > 0:
            return True
        else:
            return False

    def insert_shortcode(self, shortcode, url):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("set search_path to %(schema)s; "
                        " INSERT INTO short_codes "
                        " (short_code, url) "
                        " VALUES(%(shortcode)s, %(url)s); ",
                       {'schema': self._schema, 'shortcode': shortcode, 'url': url})
        conn.commit()
        count = cursor.rowcount
        if count > 0:
            return True
        else:
            return False