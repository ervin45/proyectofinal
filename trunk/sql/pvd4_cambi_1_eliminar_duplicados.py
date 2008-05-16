#!/usr/bin/env python
#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

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
