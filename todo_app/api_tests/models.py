
from google.appengine.api import memcache
from google.appengine.ext import ndb

class TestModel(ndb.Model):
  """A model class used for testing."""
  number = ndb.IntegerProperty(default=42)
  text = ndb.StringProperty()

class TestEntityGroupRoot(ndb.Model):
  """Entity group root"""
  pass

def GetEntityViaMemcache(entity_key):
  """Get entity from memcache if available, from datastore if not."""
  entity = memcache.get(entity_key)
  if entity is not None:
    return entity
  entity = TestModel.get(entity_key)
  if entity is not None:
    memcache.set(entity_key, entity)
  return entity