# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'bookshelf_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')(blank=True)),
        ))
        db.send_create_signal(u'bookshelf', ['Category'])

        # Adding model 'Publisher'
        db.create_table(u'bookshelf_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')(blank=True)),
        ))
        db.send_create_signal(u'bookshelf', ['Publisher'])

        # Adding model 'Author'
        db.create_table(u'bookshelf_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('fotografia', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('bio', self.gf('tinymce.models.HTMLField')(blank=True)),
        ))
        db.send_create_signal(u'bookshelf', ['Author'])

        # Adding model 'Name'
        db.create_table(u'bookshelf_name', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('syggr', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author-other-name', to=orm['bookshelf.Author'])),
        ))
        db.send_create_signal(u'bookshelf', ['Name'])

        # Adding model 'Item'
        db.create_table(u'bookshelf_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookshelf.Category'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookshelf.Publisher'], null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('bib_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('num_copies', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('num_available_copies', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('cr_code', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('notes', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('volume', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('issue', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ser_num', self.gf('django.db.models.fields.IntegerField')(max_length=255, null=True, blank=True)),
            ('num_pages', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'bookshelf', ['Item'])

        # Adding M2M table for field author on 'Item'
        m2m_table_name = db.shorten_name(u'bookshelf_item_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'bookshelf.item'], null=False)),
            ('author', models.ForeignKey(orm[u'bookshelf.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'author_id'])

        # Adding M2M table for field editor on 'Item'
        m2m_table_name = db.shorten_name(u'bookshelf_item_editor')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'bookshelf.item'], null=False)),
            ('author', models.ForeignKey(orm[u'bookshelf.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'author_id'])

        # Adding M2M table for field translator on 'Item'
        m2m_table_name = db.shorten_name(u'bookshelf_item_translator')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'bookshelf.item'], null=False)),
            ('author', models.ForeignKey(orm[u'bookshelf.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'author_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'bookshelf_category')

        # Deleting model 'Publisher'
        db.delete_table(u'bookshelf_publisher')

        # Deleting model 'Author'
        db.delete_table(u'bookshelf_author')

        # Deleting model 'Name'
        db.delete_table(u'bookshelf_name')

        # Deleting model 'Item'
        db.delete_table(u'bookshelf_item')

        # Removing M2M table for field author on 'Item'
        db.delete_table(db.shorten_name(u'bookshelf_item_author'))

        # Removing M2M table for field editor on 'Item'
        db.delete_table(db.shorten_name(u'bookshelf_item_editor'))

        # Removing M2M table for field translator on 'Item'
        db.delete_table(db.shorten_name(u'bookshelf_item_translator'))


    models = {
        u'bookshelf.author': {
            'Meta': {'object_name': 'Author'},
            'bio': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'fotografia': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'bookshelf.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bookshelf.item': {
            'Meta': {'object_name': 'Item'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'authorAsauthor'", 'blank': 'True', 'to': u"orm['bookshelf.Author']"}),
            'bib_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookshelf.Category']"}),
            'cr_code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'edition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'authorAseditor'", 'blank': 'True', 'to': u"orm['bookshelf.Author']"}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'notes': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'num_available_copies': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'num_copies': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'num_pages': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookshelf.Publisher']", 'null': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'ser_num': ('django.db.models.fields.IntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'translator': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'authorAstranslator'", 'blank': 'True', 'to': u"orm['bookshelf.Author']"}),
            'volume': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bookshelf.name': {
            'Meta': {'object_name': 'Name'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'syggr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author-other-name'", 'to': u"orm['bookshelf.Author']"})
        },
        u'bookshelf.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['bookshelf']