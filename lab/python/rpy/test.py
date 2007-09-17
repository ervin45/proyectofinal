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


