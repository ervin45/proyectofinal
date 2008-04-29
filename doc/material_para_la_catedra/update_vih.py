#!/usr/bin/env python

import MySQLdb

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="192.168.61.102", port=3306, user="proyecto", passwd="123456", db="xpweb")
cursor = con.cursor()
cursor2 = con.cursor()

project_id='1'

sql = '''
select
 id,
 name,
 description,
 load_factor
from
 iterations
where
 project_id='%s'
order by
id
 ''' % project_id
#print sql
cursor.execute(sql)

results = cursor.fetchall()
for iteracion in results:
    (iteracion_id,
     iteracion_name,
     iteracion_desc,
     load_factor) = iteracion

    t = """Iteracion: %s""" % (iteracion_name,)
    print t
    print "-" * len(t)

    print iteracion_desc
    print "\nHistorias involucradas:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    

    sql2 = '''
    select
     id,
     name,
     description,
     priority,
     risk,
     weight
    from
     stories
    where
     iteration_id = '%s'
     ''' % iteracion_id 

    cursor2.execute(sql2)
    for iteration in cursor2.fetchall():
        (iter_id,
         iter_name,
         iter_description,
         iter_prio,
         iter_risk,
         iter_weight) = iteration

        print " * ", iter_name
    print "\n\n"
        
     
