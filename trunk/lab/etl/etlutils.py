#!/usr/bin/env python


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
