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