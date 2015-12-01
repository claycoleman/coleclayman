#! /usr/bin/env python
import os, sys
from PIL import Image

dir_name = os.path.abspath(__file__).replace(os.path.basename(os.path.abspath(__file__)), "")

print dir_name




if len(sys.argv[1:]) > 0:
    onlyfiles = sys.argv[1:]
else:
    onlyfiles = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f)) and (f.lower().endswith('.png') or f.lower().endswith('.thumbnail'))]

for r in onlyfiles:
    print r

for infile in onlyfiles:
    infile = os.path.join(dir_name,infile)
    try:
        im = Image.open(infile)
        print im.size
        current_size = im.size
        im.thumbnail([current_size[0]/2, current_size[1]/2], Image.ANTIALIAS)
        im.save(infile, "PNG")
        print "New size: {}".format(im.size)
    except Exception, e:
        print e
        print "cannot create thumbnail for '%s'" % infile