# -*- coding: utf-8 -*-

# stdlib imports
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# 3rdparty imports
import Image
from uuslug import uuslug
from tinymce.models import HTMLField
from djangoratings.fields import RatingField, AnonymousRatingField
from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as TaggableManager
# app imports
from declarations import *
from south.modelsinspector import add_ignored_fields
from constance import config
import watson

## South
add_ignored_fields(["^taggit\.managers"])
add_ignored_fields(["^taggit_autocomplete_modified\.managers"])
add_ignored_fields(["^taggit_autocomplete/.managers"])


class BookNotAvailableError(Exception):
    pass

class Locations(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Τοποθεσία')
    
    
    class Meta:
        verbose_name = u"Τοποθεσία"
        verbose_name_plural = u"Τοποθεσίες"
    
    def __unicode__(self):
        return self.title
        
    def get_books_count(self):
        return Item.objects.filter(location=self).count()
    get_books_count.short_description = u"Αριθμός βιβλίων"


class Category(models.Model):
    '''
    Constructs a Category model-class containing: title-slug fields and a description field
    there is a get_books_count method and an extended save version
    '''
    
    code = models.CharField(max_length=10, verbose_name=u'Κωδικός')
    title = models.CharField(max_length=FIELD_LENGTH, verbose_name=TITLE, blank=True)
    slug = models.SlugField(max_length=FIELD_LENGTH, blank=True)
    description = HTMLField(verbose_name=DESCRIPTION, blank=True)

    class Meta:
        verbose_name = CATEGORY
        verbose_name_plural = CATEGORY_PL

    def __unicode__(self):
        if self.title:
            return self.title
        return self.code

    def save(self):
        self.slug = uuslug(self.title, instance=self)
        super(Category, self).save()

    def get_absolute_url(self):
        return ('bookshelf_categorydetail_view', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    def get_books_count(self):
        return Item.objects.filter(category=self).count()
    get_books_count.short_description = CAT_BOOKS_COUNT


class Publisher(models.Model):
    '''
    Constructs a Publisher  model-class containing: title-slug, an address and a description field
    there is a get_books_count method and an extended save version
    '''
    name = models.CharField(max_length=FIELD_LENGTH, verbose_name=NAME)
    slug = models.SlugField(max_length=FIELD_LENGTH,blank=True)
    address = models.CharField(max_length=FIELD_LENGTH,
    verbose_name=ADDRESS, blank=True)
    description = HTMLField(verbose_name=DESCRIPTION, blank=True)

    class Meta:
        verbose_name = PUBLISHER
        verbose_name_plural = PUBLISHER_PL

    def __unicode__(self):
        return self.name

    def save(self):
        self.slug = uuslug(self.name, instance=self)
        super(Publisher, self).save()

    def get_absolute_url(self):
        return ('bookshelf_publisherdetail_view', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    def get_books_count(self):
        return Item.objects.filter(publisher=self).count()
    get_books_count.short_description = PUB_BOOKS_COUNT


class Author(models.Model):
    '''
    Constructs an Author  model-class containing: title-slug, a picture and a bio field
    there is a get_books_count method and an extended save version
    '''
    name = models.CharField(max_length=FIELD_LENGTH, verbose_name=NAME)
    slug = models.SlugField(max_length=FIELD_LENGTH,blank=True)
    fotografia = models.ImageField(upload_to=AUTHOR_IMAGE, blank=True, verbose_name=IMAGE)
    bio = HTMLField(verbose_name=BIO, blank=True)

    class Meta:
        verbose_name = AUTHOR
        verbose_name_plural = AUTHOR_PL

    def __unicode__(self):
        return self.name

    def save(self):
        if self.name:
            self.slug = uuslug(self.name, instance=self)
        else:
            self.slug = 'anonymous'
        super(Author, self).save()

    def get_absolute_url(self):
        return ('bookshelf_authordetail_view', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    def get_books_count(self):
        ans = {}
        ans['asAuthor'] = Item.objects.filter(author=self).count()
        ans['asEditor'] = Item.objects.filter(editor=self).count()
        ans['asTranslator'] = Item.objects.filter(translator=self).count()
        return u"{0} (σγρφ), {1} (επιμ), {2} (μτφ)".format(ans['asAuthor'], ans['asEditor'], ans['asTranslator'])
    get_books_count.short_description = AUT_BOOKS_COUNT
    
    def get_books_asEditor(self):
        return Item.objects.filter(editor=self).count()
    get_books_asEditor.short_description = u"Ως επιμελητής"
    
    
    def get_books_asTranslator(self):
        return Item.objects.filter(translator=self).count()
    get_books_asTranslator.short_description = u"Ως μεταφραστής"
    
    def numBooks(self):
        return self.get_books_count() + self.get_books_asEditor() + self.get_books_asTranslator()
    numBooks.short_description = u'Αριθμός βιβλίων'


class Name(models.Model):
    name = models.CharField(max_length=FIELD_LENGTH, verbose_name=NAME)
    syggr = models.ForeignKey("Author", related_name="author-other-name")

    class Meta:
        verbose_name = u"Άλλο όνομα"
        verbose_name_plural = u"Άλλα ονόματα"

    def __unicode__(self):
        return self.name
        
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(published=True)

class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(status=True)

                
class Item(models.Model):
    '''
    Constructs an Item  model-class containing:
    '''
    ## Non-optional
    
    
    ## na valw kai xrhsimes ypersyndeseis kai edw kai ston syggrafea

    ## Basic
    title = models.CharField(max_length=FIELD_LENGTH, verbose_name=TITLE)
    machine_name = models.CharField(max_length=255, verbose_name=u"Εσωτερικός Τίτλος")
    slug = models.SlugField(max_length=FIELD_LENGTH,blank=True)
    author = models.ManyToManyField("Author", verbose_name=AUTHOR, related_name="authorAsauthor", blank=True)
    language = models.CharField(max_length=2, verbose_name=LANGUAGE, choices=LANGUAGES, blank=True)
    category = models.ForeignKey("Category", verbose_name=CATEGORY, null = True, blank=True)
    publisher = models.ForeignKey("Publisher", verbose_name=PUBLISHER, null=True, blank=True)

    ## Bib Info
    status = models.BooleanField(default=True, verbose_name=AVAILABLE, null=False)
    cr_code = models.IntegerField(verbose_name=CR_CODE, unique=True)
    bib_code = models.CharField(max_length=FIELD_LENGTH, verbose_name=BIB_CODE)
    published = models.BooleanField(default=True, verbose_name=u"Δημοσιευμένο", null=False)
    num_copies = models.PositiveIntegerField(default=1, verbose_name=NUM_COPIES)
    num_available_copies = models.PositiveIntegerField(default=1, verbose_name=u"Αριθμός διαθέσιμων βιβλίων")
    isbn = models.PositiveIntegerField(blank=True, null=True)
    parapanw_antitypo = models.BooleanField(default=False, verbose_name=u"Παραπανίσιο αντίτυπο", null=False)


    ## Optional
    year = models.PositiveIntegerField(blank=True, verbose_name=YEAR, null=True)
    foto = models.ImageField(upload_to=BOOK_IMAGE, blank=True, verbose_name=IMAGE)
    tags = TaggableManager(blank=True, verbose_name=KEYWORDS, help_text=u"Διαχωρίστε τις λέξεις-κλειδιά με κόμμα. <b>Σημ: το κενό (space) δημιουργεί φράση-κλειδί</b>")
    notes = HTMLField(blank=True, verbose_name=NOTES)
    issue = models.IntegerField(verbose_name=ISSUE, blank=True, null=True)
    editor = models.ManyToManyField("Author", verbose_name=EDITOR, related_name="authorAseditor", blank=True)
    rating = RatingField(range=5)
    series = models.CharField(verbose_name=SERIES, max_length=255, blank=True)
    volume = models.IntegerField(verbose_name=VOLUME, blank=True, null=True)
    ser_num = models.IntegerField(verbose_name=SER_NUM, max_length=255, blank=True, null=True)
    edition = models.IntegerField(verbose_name=EDITION, blank=True, null=True, help_text=u"Εισάγετε τον αριθμό της έκδοσης, πχ. <b>3</b> ώστε να εμφανιστεί <em>3η έκδοση</em>")
    abstract = HTMLField(verbose_name=u'Περίληψη', blank =True)
    subtitle = models.CharField(max_length=FIELD_LENGTH, verbose_name=SUBTITLE, blank=True)
    proelefsi = models.CharField(max_length=FIELD_LENGTH, verbose_name=u'Προέλευση', blank=True)
    num_pages = models.PositiveIntegerField(blank=True, verbose_name=PAG_NUM, null=True)
    translator = models.ManyToManyField("Author", verbose_name=TRANSLATOR, related_name="authorAstranslator", blank=True)
    location = models.ForeignKey("Locations", null=True, blank=True, verbose_name=u"Τοποθεσία")
    objects = models.Manager()
    published_books = PublishedManager()
    available_books = AvailableManager()

    class Meta:
        verbose_name = ITEM
        verbose_name_plural = ITEM_PL

    def __unicode__(self):
        if self.subtitle:
            return self.machine_name + ': ' + self.subtitle
        else:
            return self.machine_name

    def save(self):
        if self.num_available_copies < 0:
            raise BookNotAvailableError
        elif self.num_available_copies == 0:
            self.status = False
            
        if not self.pk:
            other_copies = len(Item.objects.filter(title=self.title))
            if other_copies:
                self.parapanw_antitypo = True
            if self.parapanw_antitypo:
                self.machine_name = self.title + u' (αντ. {0})'.format(other_copies + 1)
                ## find the only published
                for book in Item.objects.filter(title=self.title):
                    if book.parapanw_antitypo == False:
                        book.num_copies += 1
                        book.num_available_copies += 1
                        book.save()
            else:
                self.machine_name = self.title + u' (αντ. 1)'
        self.slug = uuslug(self.title, instance=self)
        super(Item, self).save()

    def get_absolute_url(self):
        return ('bookshelf_itemdetail_view', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    def get_book_authors(self):
        return ', '.join(author.name for author in self.author.all())

    def get_authors(self):
        return ', '.join([a.name for a in self.author.all()])
    get_authors.short_description = AUTHOR_PL

    def get_editors(self):
        return ', '.join([a.name for a in self.editor.all()])

    def get_publishers(self):
        return ', '.join([p.name for p in self.publisher.objects.all()])

    def clean(self):
        if self.num_available_copies > self.num_copies:
            raise ValidationError(ITEM_VAL_ERR)

watson.register(Author)
watson.register(Item)