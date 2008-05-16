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
 
# a bar plot with errorbars
# a bar plot with errorbars
from pylab import *

N = 5
menMeans = (20, 35, 30, 35, 27)
menStd =   ( 2,  3,  4,  1,  2)

ind = arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
p1 = bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (25, 32, 34, 20, 25)
womenStd =   ( 3,  5,  2,  3,  3)
p2 = bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

ylabel('Scores')
title('Scores by group and gender')
xticks(ind+width, ('G1', 'G2', 'G3', 'G4', 'G5') )
xlim(-width,len(ind))
yticks(arange(0,41,10))

legend( (p1[0], p2[0]), ('Men', 'Women'), shadow=True)
show()#############################################################################
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
 
# a bar plot with errorbars
# a bar plot with errorbars
from pylab import *

N = 5
menMeans = (20, 35, 30, 35, 27)
menStd =   ( 2,  3,  4,  1,  2)

ind = arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
p1 = bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (25, 32, 34, 20, 25)
womenStd =   ( 3,  5,  2,  3,  3)
p2 = bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

ylabel('Scores')
title('Scores by group and gender')
xticks(ind+width, ('G1', 'G2', 'G3', 'G4', 'G5') )
xlim(-width,len(ind))
yticks(arange(0,41,10))

legend( (p1[0], p2[0]), ('Men', 'Women'), shadow=True)
show()