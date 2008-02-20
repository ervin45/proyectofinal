#!/usr/bin/env python
import datetime
import MySQLdb

## llamarlo de la siguiente manera
## for a in `seq 1 13`; do ./pvd4_cambi_2_completa_faltantes.py | tee completa_faltantes$a.sql| mysql -u root b2; done




# Create a connection object and create a cursor
con = MySQLdb.Connect(host="localhost", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor()


sql = '''select max(CAM_COMPRA) as maxima,CAM_FECHA, CAM_COMPRA, CAM_VENDED, fecha    from PVD4_CAMBI group by CAM_FECHA order by fecha'''


cursor.execute(sql)

results = cursor.fetchall()
for row in results:
    next_day = row[4] + datetime.timedelta(1,0,0)
    sql = '''select * from PVD4_CAMBI where fecha = '%s' ''' % str(next_day)
    if cursor.execute(sql) == 0:
        print '''insert into PVD4_CAMBI (CAM_FECHA, CAM_COMPRA, CAM_VENDED, fecha) values ('%s',%.2f,%.2f,'%s' );''' % (next_day.strftime('%y%m%d'),row[2],row[3],str(next_day))

