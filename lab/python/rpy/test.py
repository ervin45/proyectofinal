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
from rpy import *
import math

x = range(0, 10)
y1 = [ 2*i for i in x ]
y2 = [ math.log(i+1) for i in x ]
outfile = "imagen.png"
r.bitmap(outfile, res=200)

f = ("a","b","a","c","c","a","b","a","a")

#r.plot_default(f)
r.plot_default(x, y1, col="blue", type="o")
#r.points(x, y2, col="red", type="o")

#xlabels = [ "#%d" % (i,) for i in x ]
#r.axis(1, at = x, label=xlabels, lwd=1, cex_axis=1.15)
#r.title("My Plot")


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
from rpy import *
import math

x = range(0, 10)
y1 = [ 2*i for i in x ]
y2 = [ math.log(i+1) for i in x ]
outfile = "imagen.png"
r.bitmap(outfile, res=200)

f = ("a","b","a","c","c","a","b","a","a")

#r.plot_default(f)
r.plot_default(x, y1, col="blue", type="o")
#r.points(x, y2, col="red", type="o")

#xlabels = [ "#%d" % (i,) for i in x ]
#r.axis(1, at = x, label=xlabels, lwd=1, cex_axis=1.15)
#r.title("My Plot")


