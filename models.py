from google.appengine.ext import ndb


class Sporocilo(ndb.Model):
    ime = ndb.StringProperty()
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
