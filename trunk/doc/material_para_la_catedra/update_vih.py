#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import MySQLdb

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="192.168.61.102", port=3306, user="proyecto", passwd="123456", db="xpweb")
cursor = con.cursor()
cursor2 = con.cursor()

project_id='1'

d = { '1.0': [4, 1],
     
      }

a = [('Versi�n 1.0', [4, 1]),
     ('Versi�n 2.0', [5, 6, 2]),
     ('Versi�n 3.0', [7, 8, 3]),
     ('Versi�n 4.0', [9,10,11]),
     ('Versi�n 5.0', [12])]


for (version_id, iterations)  in a:

    print "-" * len(version_id)
    print version_id
    print "-" * len(version_id)
    print


    for iteration in iterations:

        sql = '''
        select
         id,
         name,
         description,
         load_factor
        from
         iterations
        where
         project_id='%s' and
         id='%d'

         ''' % (project_id, iteration)
        #print sql
        cursor.execute(sql)

        results = cursor.fetchall()


        for iteracion in results:
            (iteracion_id,
             iteracion_name,
             iteracion_desc,
             load_factor) = iteracion

            t = """Iteraci�n: %s""" % (iteracion_name,)
            print t
            print "-" * len(t)

            print iteracion_desc
            #print "\nHistorias involucradas:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            print "\nHistorias involucradas:\n\n"


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

                print ":%s: %s" %( iter_name, iter_description)
                print
                
            print "\n\n"



h = "Historias fuera de iteraciones:"
print "-" * len(h)
print h
print "-" * len(h)
print


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
 iteration_id = '0'
 '''

cursor2.execute(sql2)
for iteration in cursor2.fetchall():
    (iter_id,
     iter_name,
     iter_description,
     iter_prio,
     iter_risk,
     iter_weight) = iteration

    print ":%s: %s" %( iter_name, iter_description)
    print

print "\n\n"


