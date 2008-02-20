#!/usr/bin/env python

import MySQLdb

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="localhost", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor()

sql = '''select max(CAM_COMPRA) as maxima,CAM_FECHA, CAM_COMPRA, CAM_VENDED, fecha    from PVD4_CAMBI group by CAM_FECHA order by fecha'''
cursor.execute(sql)

print '''truncate PVD4_CAMBI;'''

results = cursor.fetchall()
for row in results:
    print '''insert into PVD4_CAMBI (CAM_FECHA, CAM_COMPRA, CAM_VENDED, fecha) values ('%s',%.2f,%.2f,'%s' );''' % (row[1],row[2],row[3],str(row[4]))

print '''create unique index fecha on PVD4_CAMBI(fecha);'''
