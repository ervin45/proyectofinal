#DATABASE_HOST = '192.168.61.102'
DATABASE_HOST = 'localhost'

def cursor():
    import psycopg2
    import psycopg2.extras
    con = psycopg2.connect(host=DATABASE_HOST, port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
    return con.cursor(cursor_factory=psycopg2.extras.DictCursor) 