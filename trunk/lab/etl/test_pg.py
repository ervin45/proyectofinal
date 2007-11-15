#!/usr/bin/env python

#from pyPgSQL import PgSQL
import psycopg2 as  PgSQL


con_dwh = PgSQL.connect(host="192.168.61.102", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
cursor_dwh = con_dwh.cursor()


sql = "select id from td_tiempo where anio = '1945' and mes = '5'"

for a in range(180):
    cursor_dwh.execute (sql)
    print a, cursor_dwh.fetchone ()
