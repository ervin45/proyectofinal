#!/usr/bin/env python


def get_id(cursor, tabla, campoid, campos, filtro=None):

	print "10"
        if filtro:
                rtn = {}
                for x in campos:
                        if x in filtro:
                                rtn[x] = campos[x]
                campos = rtn


	print "20"
        sql = "select %s from %s where " % (campoid, tabla)
        arr = []
	print "30"
        for k in campos.keys():
                arr.append("%s = '%s'" % (k, campos[k]))

	print "40"
        sql += ' and '.join(arr)

        sql_select = sql
	print "50 / %s %% %s" % (sql, ", ".join([str(x) for x in campos.values()]))
        #cursor.execute (sql, campos.values())
        cursor.execute (sql)
	print "60"

        try:
		print "70"
		rtn = cursor.fetchone ()[campoid]
        except:
		print "80"

                sql = "insert into %s (%s) values (%s)" % (tabla, ', '.join(campos.keys()), ', '.join(['%s' for x in campos.values()]))
                print sql
                cursor.execute (sql, campos.values())
		print "90"
                #cursor.execute (sql_select, campos.values())
		cursor.execute (sql_select)
                rtn = cursor.fetchone ()[campoid]
		print "100"
	print "101"
        return rtn
