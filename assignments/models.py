# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from uuslug import uuslug
from bookshelf.models import Item


class Assignment(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Τίτλος εργασίας')
    slug = models.SlugField(blank=True)
    participants = models.ManyToManyField(User, verbose_name=u'Μαθητές')
    book = models.ForeignKey(Item, verbose_name=u'Βιβλίο')
    file = models.FileField(upload_to="/assignments", blank=True, null=True, verbose_name=u'Αρχείο')
    created_at  = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Δημιουργήθηκε στις')
    description = models.TextField(blank=True, verbose_name=u"Περιγραφή")


    class Meta:
        verbose_name = u'Εργασία'
        verbose_name_plural = u'Εργασίες'
        
    def __unicode__(self):
        return "%s: %s" % (self.get_participants(), self.book.title)
        
    def save(self):
        self.slug = uuslug(self.title, instance=self)
        super(Assignment, self).save()
        
    def get_absolute_url(self):
        return ('assignments_assignmentdetail_view', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)    
    
    def get_participants(self):
        return ', '.join(participant.username for participant in self.participants.all())
        
    def get_school_year(self):
        return str(self.created_at.year - 1) + "/" + str(self.created_at.year)