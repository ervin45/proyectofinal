#!/usr/bin/python

from olap import cubiculo
from olap import reports

instance_type = type(cubiculo.Cubiculo._select), type(cubiculo.Meta.previous) 

classes = [(cubiculo.Cubiculo, "cubiculo.Cubiculo"), (cubiculo.Meta, "cubiculo.Meta"), (reports.Cube, "reports.Cube"), (reports.Report1, "reports.Report1"), (reports.Report2, "reports.Report2"), (reports.Ajax_responser, "reports.Ajax_responser")]

for c in classes:

    print "Clase: %s"  % c[1]
    print "--------------------------------"
    print ""

    for a in [x for x in dir(c[0]) if x not in('__doc__', '__module__')]:
        if type(eval('%s.%s' %  (c[1], a) ) ) in(instance_type):
            eval_doc = eval('%s.%s.__doc__' % (c[1], a) )
            eval_name = eval('%s.%s.__name__'  % (c[1], a) )
            if eval_doc != None:

                print 'Metodo: %s' % eval_name
                print '%s' % eval_doc