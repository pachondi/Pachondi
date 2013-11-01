# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteUser'
        db.create_table(u'users_siteuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('user_slug', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('dob', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 10, 28, 0, 0))),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invalid_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lock_expires_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('is_show_viewers_also_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'users', ['SiteUser'])

        # Adding M2M table for field groups on 'SiteUser'
        m2m_table_name = db.shorten_name(u'users_siteuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('siteuser', models.ForeignKey(orm[u'users.siteuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['siteuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'SiteUser'
        m2m_table_name = db.shorten_name(u'users_siteuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('siteuser', models.ForeignKey(orm[u'users.siteuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['siteuser_id', 'permission_id'])

        # Adding model 'UserEmail'
        db.create_table(u'users_useremail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.SiteUser'])),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['UserEmail'])

        # Adding model 'UserWebsites'
        db.create_table(u'users_userwebsites', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.SiteUser'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['UserWebsites'])

        # Adding model 'Skill'
        db.create_table(u'users_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'users', ['Skill'])

        # Adding model 'UserSkills'
        db.create_table(u'users_userskills', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.SiteUser'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Skill'])),
            ('skill_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'users', ['UserSkills'])

        # Adding model 'UserRecommendation'
        db.create_table(u'users_userrecommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.SiteUser'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('recommender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recommended_by', to=orm['users.SiteUser'])),
            ('recommended_as', self.gf('django.db.models.fields.IntegerField')()),
            ('recommend_basis', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('recommender_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'users', ['UserRecommendation'])


    def backwards(self, orm):
        # Deleting model 'SiteUser'
        db.delete_table(u'users_siteuser')

        # Removing M2M table for field groups on 'SiteUser'
        db.delete_table(db.shorten_name(u'users_siteuser_groups'))

        # Removing M2M table for field user_permissions on 'SiteUser'
        db.delete_table(db.shorten_name(u'users_siteuser_user_permissions'))

        # Deleting model 'UserEmail'
        db.delete_table(u'users_useremail')

        # Deleting model 'UserWebsites'
        db.delete_table(u'users_userwebsites')

        # Deleting model 'Skill'
        db.delete_table(u'users_skill')

        # Deleting model 'UserSkills'
        db.delete_table(u'users_userskills')

        # Deleting model 'UserRecommendation'
        db.delete_table(u'users_userrecommendation')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.siteuser': {
            'Meta': {'object_name': 'SiteUser'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dob': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 28, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalid_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_show_viewers_also_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'lock_expires_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_slug': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'users.skill': {
            'Meta': {'object_name': 'Skill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'users.useremail': {
            'Meta': {'object_name': 'UserEmail'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.SiteUser']"})
        },
        u'users.userrecommendation': {
            'Meta': {'object_name': 'UserRecommendation'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'recommend_basis': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'recommended_as': ('django.db.models.fields.IntegerField', [], {}),
            'recommender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recommended_by'", 'to': u"orm['users.SiteUser']"}),
            'recommender_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.SiteUser']"}),
            'user_title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'users.userskills': {
            'Meta': {'object_name': 'UserSkills'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Skill']"}),
            'skill_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.SiteUser']"})
        },
        u'users.userwebsites': {
            'Meta': {'object_name': 'UserWebsites'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.SiteUser']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['users']