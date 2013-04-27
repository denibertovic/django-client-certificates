# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Cert.locality'
        db.alter_column(u'client_certs_cert', 'locality', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Cert.country'
        db.alter_column(u'client_certs_cert', 'country', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Cert.state'
        db.alter_column(u'client_certs_cert', 'state', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Cert.organizational_unit'
        db.alter_column(u'client_certs_cert', 'organizational_unit', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Cert.common_name'
        db.alter_column(u'client_certs_cert', 'common_name', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Cert.organization'
        db.alter_column(u'client_certs_cert', 'organization', self.gf('django.db.models.fields.CharField')(max_length=64))

    def backwards(self, orm):

        # Changing field 'Cert.locality'
        db.alter_column(u'client_certs_cert', 'locality', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Cert.country'
        db.alter_column(u'client_certs_cert', 'country', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Cert.state'
        db.alter_column(u'client_certs_cert', 'state', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Cert.organizational_unit'
        db.alter_column(u'client_certs_cert', 'organizational_unit', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Cert.common_name'
        db.alter_column(u'client_certs_cert', 'common_name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Cert.organization'
        db.alter_column(u'client_certs_cert', 'organization', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'client_certs.cert': {
            'Meta': {'object_name': 'Cert'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'export_password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organizational_unit': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'x509': ('django.db.models.fields.TextField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['client_certs']