#!/usr/bin/python

from olap import cubiculo
from olap import reports

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

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
                print "\n".join(["          %s" % x.strip() for x in wrap(eval_doc, 40).split("\n")])