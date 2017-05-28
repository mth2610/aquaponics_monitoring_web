from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Sites(object):
    def __init__(self,**kwargs):
        for field, value in kwargs.iteritems():
            if field != '_id':
                setattr(self, field, value)
            else:
                setattr(self, 'id', str(value))

class DataValues(object):
    def __init__(self,**kwargs):
        for field, value in kwargs.iteritems():
            if field != '_id':
                setattr(self, field, value)
            else:
                setattr(self, 'id', str(value))

class Images(object):
    def __init__(self,**kwargs):
        for field, value in kwargs.iteritems():
            if field != '_id':
                setattr(self, field, value)
            else:
                setattr(self, 'id', str(value))
