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


def get_id(cursor, tabla, campoid, campos, filtro=None):

        if filtro:
                rtn = {}
                for x in campos:
                        if x in filtro:
                                rtn[x] = campos[x]
                campos = rtn


        sql = "select %s from %s where " % (campoid, tabla)
        arr = []
        for k in campos.keys():
                arr.append("%s = %%s" % k)

        sql += ' and '.join(arr)

        sql_select = sql
        cursor.execute (sql, campos.values())

        try:
		rtn = cursor.fetchone ()[0]
        except:		
                sql = "insert into %s (%s) values (%s)" % (tabla, ', '.join(campos.keys()), ', '.join(['%s' for x in campos.values()]))
		print sql, campos.values()
		try:
			cursor.execute ("commit")
		except:
			pass

                cursor.execute (sql, campos.values())
		cursor.execute (sql_select, campos.values())
                rtn = cursor.fetchone ()[0]
        return rtn
