# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User

from uuslug import uuslug
from tinymce.models import HTMLField

from bookshelf.models import Item

class BookList(models.Model):
    title       = models.CharField(verbose_name=u"Τίτλος Λίστας",max_length=255)
    slug        = models.SlugField(max_length=255, blank=True)
    user        = models.ForeignKey(User,verbose_name=u"Όνομα Χρήστη")
    books       = models.ManyToManyField(Item,verbose_name=u"Βιβλία", blank=True, null=True)
    public      = models.BooleanField(verbose_name=u"Δημόσια",default=True, help_text=u"Αυτή τη λίστα θα μπορούν να τη βλέπουν και άλλοι χρήστες της βιβλιοθήκης.")
    created_at  = models.DateTimeField(verbose_name=u"Δημιουργήθηκε",auto_now_add=True, editable=False)
    updated_at  = models.DateTimeField(verbose_name=u"Ανανεώθηκε",auto_now=True, editable=False)
    likes       = models.PositiveIntegerField(verbose_name=u"Ψήφοι",default=0, blank=True)
    description = HTMLField(blank=True, verbose_name=u"Περιγραφή της λίστας")
    image       = models.ImageField(verbose_name=u"Εικόνα της λίστας", upload_to="lists/",blank=True)
    
    class Meta:
        verbose_name = u'Λίστα'
        verbose_name_plural = u'Λίστες'

    def __unicode__(self):
        return "%s: %s" % (self.user.username, self.title)
        
    def save(self):
        self.slug = uuslug(self.title, instance=self)
        super(BookList, self).save()

    def get_absolute_url(self):
        return ('lists_view_list', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_book_count(self):
        return self.books.count()
    get_book_count.short_description = u"Αριθμός Βιβλίων"