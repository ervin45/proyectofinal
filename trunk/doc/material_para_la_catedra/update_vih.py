#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
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
con = MySQLdb.Connect(host="192.168.61.101", port=3306, user="proyecto", passwd="123456", db="xpweb")
cursor = con.cursor()
cursor2 = con.cursor()

project_id='1'

d = { '1.0': [4, 1],
     
      }

a = [('Versión 1.0', [4, 1]),
     ('Versión 2.0', [5, 6, 2]),
     ('Versión 3.0', [7, 8, 3]),
     ('Versión 4.0', [9,10,11]),
     ('Versión 5.0', [12])]


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

            t = """Iteración: %s""" % (iteracion_name,)
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

                print ":[#%d] %s: %s" %(iter_id, iter_name, iter_description)
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

    print ":[#%d] %s: %s" %(iter_id, iter_name, iter_description)
    print

print "\n\n"


