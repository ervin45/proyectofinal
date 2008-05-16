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

#from pyPgSQL import PgSQL
import psycopg2 as  PgSQL


con_dwh = PgSQL.connect(host="192.168.61.102", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
cursor_dwh = con_dwh.cursor()


sql = "select id from td_tiempo where anio = '1945' and mes = '5'"

for a in range(1800):
    cursor_dwh.execute (sql)
    print a, cursor_dwh.fetchone ()
