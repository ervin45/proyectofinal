#!/usr/bin/env python

import MySQLdb

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="192.168.61.100", port=3306, user="proyecto", passwd="123456", db="xpweb")
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
for version in results:
    (version_id,
     version_name,
     version_desc,
     load_factor) = version

    t = """Version %s: %s""" % (version_id, version_name)
    print t
    print "=" * len(t)
    

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
     ''' % version_id 

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
        
     
