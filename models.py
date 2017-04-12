from google.appengine.ext import ndb

class Movies(ndb.Model):
    name = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    information = ndb.StringProperty()
    image = ndb.StringProperty()
    average_rating_str = ndb.StringProperty()
    average_rating_float_list = ndb.FloatProperty(repeated=True)
    average_rating_float_in_str = ndb.StringProperty()
    number_of_ratings = ndb.StringProperty()
    number_of_excellent_ratings_str = ndb.StringProperty()
    number_of_very_good_ratings_str = ndb.StringProperty()
    number_of_good_ratings_str = ndb.StringProperty()
    number_of_not_special_ratings_str = ndb.StringProperty()
    number_of_bad_ratings_str = ndb.StringProperty()
    comments = ndb.StringProperty(repeated=True)
    author = ndb.StringProperty(repeated=True)
