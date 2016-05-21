# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, re, sys
from bookshelf.models import Author, Item, Publisher, Category, Locations

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

print "Reading files...",

BASE_DIR = '/Users/dimitriosalikaniotis/Projects/vivliothiki'

## get db
DATABASE_FILE = os.path.join(BASE_DIR, 'lib2.txt') ## csv file
CATEGORIES_FILE = open(os.path.join(BASE_DIR, 'categories.txt'), 'r') ## categories file
AUTHORS_FILE = open(os.path.join(BASE_DIR, 'syggrafeas.txt'), 'r')
PUBLISHERS_FILE = open(os.path.join(BASE_DIR, 'publishers.txt'), 'r')


f = CATEGORIES_FILE.read()
CATEGORIES_FILE.close()
f = f.decode('utf-8')
cat_dict = {code: description for code, description in [x.split(',') for x in f.split('\n')]}

authors = AUTHORS_FILE.read()
AUTHORS_FILE.close()
authors = authors.decode('utf-8')
authors = authors.split('\n')

publishers = PUBLISHERS_FILE.read()
PUBLISHERS_FILE.close()
publishers = publishers.decode('utf-8')
publishers = publishers.split('\n')

print "Done!"
## PREPROCESS
## CATEGORIES
def makeCategories():
    for i, (c, d) in enumerate(cat_dict.items(), 1):
        ##
        print "\r >> Done {0} / {1} categories ({2:.2f}%)".format(i,
            len(cat_dict.keys()), i / float(len(cat_dict.keys())) * 100),
        sys.stdout.flush()
        ##
        category = Category()
        category.code = c
        category.title = d
        category.save()
## AUTHORS
def makeAuthors():
    for i, a in enumerate(authors, 1):
        ##
        print "\r >> Done {0} / {1} authors ({2:.2f}%)".format(i,
            len(authors), i / float(len(authors)) * 100),
        sys.stdout.flush()
        ##
        auth = Author()
        auth.name = a
        auth.save()
## PUBLISHERS
def makePublishers():
    for i, p in enumerate(publishers, 1):
        ##
        print "\r >> Done {0} / {1} publishers ({2:.2f}%)".format(i,
            len(publishers), i / float(len(publishers)) * 100),
        sys.stdout.flush()
        ##
        pub = Publisher()
        pub.name = p
        pub.save()




LOCATION = Locations()
LOCATION.title = u"Βιβλιοθήκη"
LOCATION.save()

class MyDatabase(object):
    def __init__(self, csv):
        self.csv = csv
    def __iter__(self):
        with open(self.csv) as dbase:
            for line in dbase:
                line = line.decode('utf-8')
                yield line.rstrip('\n').split('\t')

database = MyDatabase(DATABASE_FILE)
N = 0
for l in database: N += 1

print '\nMaking Categories'
makeCategories()
print '\nMaking Authors'
makeAuthors()
print '\nMaking Publishers'
makePublishers()
print '\nMaking Books'
for i, line in enumerate(database, 1):
    ##
    print "\r >> Done {0} / {1} books ({2:.2f}%)".format(i,
        N, i / float(N) * 100),
    sys.stdout.flush()
    ##
    try:
        ar_eis, lekseis_kleidia, titlos, syggrafeas, ar_ekd, dimosiefsi, ekdosi, metafrastis, vivliarithmos, shmeiwseis, de_vrethike, diathesimothta, proelefsi, xwros = line
        myre = re.compile(ur'\s*\u03b1\u03bd\u03c4\s?\.\s?\d{1}\s*', re.UNICODE)
        titlos = myre.sub('', titlos)
        titlos = unicode(titlos)
            
        kathgoria = vivliarithmos[:vivliarithmos.find('/')]
        year_re = re.search('\d{4}', dimosiefsi)
        try:
            year = year_re.group(0)
        except AttributeError:
            year = ''
        kwd_eis = int(ar_eis)
        tags = lekseis_kleidia.split(',')
        try:
            author = Author.objects.get(name=syggrafeas)
        except Author.MultipleObjectsReturned:
            author = Author.objects.filter(name=syggrafeas)[0]
        except Author.DoesNotExist:
            author = Author()
            author.name = syggrafeas
            author.save()
        try:
            category = Category.objects.get(code=kathgoria)
        except Category.MultipleObjectsReturned:
            category = Category.objects.filter(code=kathgoria)[0]
        except Category.DoesNotExist:
            category = Category()
            category.code = kathgoria
            category.save()
        try:
            publisher = Publisher.objects.get(name=ekdosi)
        except Publisher.MultipleObjectsReturned:
            publisher = Publisher.objects.filter(name=ekdosi)[0]
        except Publisher.DoesNotExist:
            publisher = Publisher()
            publisher.name = ekdosi
            publisher.save()
        item = Item()
        item.cr_code = kwd_eis
        item.bib_code = vivliarithmos
        if not titlos:
            titlos = u'Χωρίς τίτλο'
        item.title = titlos
        item.save()
        item.notes = shmeiwseis
        item.proelefsi = proelefsi
        if year:
            item.year = year
        item.location = LOCATION
        item.tags.add(*tags)
        if u'επιμ' in syggrafeas:
            item.editor.add(author)
        else:
            item.author.add(author)
        if metafrastis:
            try:
                trans = Author.objects.get(name=metafrastis)
            except Author.MultipleObjectsReturned:
                author = Author.objects.filter(name=metafrastis)[0]
            except Author.DoesNotExist:
                trans = Author()
                trans.name = metafrastis
                trans.save()
            item.translator.add(trans)
        item.category = category
        item.publisher = publisher
        item.save()

    except ValueError:
        print u'Πρόβλημα στην εγγραφή {0}'.format(line[0])
    
print "Success!"