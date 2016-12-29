#! /usr/bin/env python

import os, sys
import datetime
import unidecode

proj_path = os.path.join(os.path.dirname(__file__), '..')
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.append(proj_path)

import django, re
django.setup()


from portfolio.models import *

# dc > 3
# ot > 2
# nt > 1
# pgp > 2
# bom > 8 && bom < 248

dbs = [
    ['bom', 8, 248],
    ['dc', 3, False],
    ['ot', 2, False],
    ['nt', 1, False],
    ['pgp', 2, False],
]


import sqlite3

for db in dbs:
    conn = sqlite3.connect('%s.sqlite' % db[0])
    c = conn.cursor()
    command = 'SELECT subitem.*, subitem_content.* FROM subitem INNER JOIN subitem_content ON (subitem._id = subitem_content._id) WHERE subitem._id > %s' % db[1]
    if db[2]:
        command += " AND subitem._id < %s" % db[2]

    print command

    for row in c.execute(command):
        title = unidecode.unidecode(row[3])
        url = unidecode.unidecode(row[5])
        book = db[0] 
        book = "bible" if book == 'ot' or book == 'nt' else book
        
        new_scrip, created = ScriptureCache.objects.get_or_create(chapter_title=title, book_of_scripture=book)
        new_scrip.web_url = url
        new_scrip.save()
        print title

        content = str(row[-1])
        m = re.findall(r'data-page="(\d+)"', content)
        
        for match in m:
            print match
            new_page_num, created = PageNumber.objects.get_or_create(scripture=new_scrip, page_number=match)

    conn.close()

sys.exit()