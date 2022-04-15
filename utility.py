from configparser import ConfigParser
import psycopg2
import logging

def read_db_config(filename = 'database.ini', section = 'quiz_postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        e = Exception('Section {0} not found in the {1} file'.format(section, filename))
        logging.info(f'{e}')
        raise e

    return db

def connect_test(db_config):
    conn = None
    try:
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        logging.info(f'PostgreSQL database version: "{db_version}"!')
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        logging.info(f'PostgreSQL database version: "{e}"!')
    finally:
        if conn is not None:
          conn.close()
          logging.debug('Database connection closed.')
