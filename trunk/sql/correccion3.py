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
## executed as:
## ./correccion3.py | iconv --from-code=cp850 --to-code=utf8| psql -h 192.168.61.100 -U ncesar bieler_dw


import datetime
import MySQLdb

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="localhost", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor()


sql = '''select  PRO_NOMBRE, PRO_NUMERO from PVD3_PROVE'''


cursor.execute(sql)

results = cursor.fetchall()
for row in results:
    print '''update td_proveedor set proveedor='%s' where id_octosis='%s';''' % (row[0].strip(), row[1])

