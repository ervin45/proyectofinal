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


#!/usr/bin/env python

import sys

if not len(sys.argv) == 2:
    print "usage:"
    print "   add_gpl.py file.py"
    print
    sys.exit()

gpl = '''#############################################################################
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
#############################################################################'''

#make it a list
gpl = [x+"\n" for x in gpl.splitlines()]

filename  = sys.argv[1]
filename2 = filename+".bak"

input=file(filename,"r")


all_the_file=input.readlines()

if len(all_the_file) == 0:
    print "%s es un archivo vacio" % filename
    sys.exit()

def ya_la_tiene(all_the_file):
    largo = len(gpl)
    for i in range(len(all_the_file) - largo):
        t = all_the_file[i:i+largo]
        if t == gpl:
            return True
    return False

if ya_la_tiene(all_the_file):
    print "%s ya tiene la GPL." % filename
else:
    print "%s no tiene la GPL." % filename
    output=file(filename2,"w")

    offset = 0
    if all_the_file[0].startswith("#!"):
        offset = 1
        if all_the_file[1].startswith("# -*- coding:"):
            offset = 2
    else:
        output.writelines(gpl + all_the_file)

    output.writelines(all_the_file[0:offset] + gpl + all_the_file[offset:])

    print "Se escribio %s con la GPL" % filename2


