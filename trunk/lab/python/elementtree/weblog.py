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
#from elementtree import ElementTree
import cElementTree as ElementTree

weblog = ElementTree.parse('weblog.xml').getroot()
interesting = [entry for entry in weblog.findall('entry') if entry.find('host').text=='209.202.148.31' and entry.find('statusCode').text=='200']

for e in interesting:
  print "%s (%s)" % (e.findtext('resource'), e.findtext('byteCount'))
  
e = weblog.getiterator('dateTime')
for a in e:
    pass
    #print a.text
    
atomg = ElementTree.parse('/home/chinomng/utn/proyecto/proyectofinal/lab/python/elementtree/atomg.xml').getroot()
print weblog
print atomg

author = atomg.getiterator('author')
for a in author:
    print a#############################################################################
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
#from elementtree import ElementTree
import cElementTree as ElementTree

weblog = ElementTree.parse('weblog.xml').getroot()
interesting = [entry for entry in weblog.findall('entry') if entry.find('host').text=='209.202.148.31' and entry.find('statusCode').text=='200']

for e in interesting:
  print "%s (%s)" % (e.findtext('resource'), e.findtext('byteCount'))
  
e = weblog.getiterator('dateTime')
for a in e:
    pass
    #print a.text
    
atomg = ElementTree.parse('/home/chinomng/utn/proyecto/proyectofinal/lab/python/elementtree/atomg.xml').getroot()
print weblog
print atomg

author = atomg.getiterator('author')
for a in author:
    print a