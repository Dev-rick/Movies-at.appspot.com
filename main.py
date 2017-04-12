# -*- coding: utf-8 -*-
import webapp2
import os
import jinja2
from models import Movies
import counter


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainPage(BaseHandler):
    def get(self):
        movies = Movies.query().fetch()
        params = {"movies": movies}
        return self.render_template("home.html", params)


class ResultHandler(BaseHandler):
    def post(self):
        name = self.request.get("name")
        information = self.request.get("information")
        image = self.request.get("image")
        bad = self.request.get("bad")
        not_special = self.request.get("not_special")
        good = self.request.get("good")
        very_good = self.request.get("very_good")
        excellent = self.request.get("excellent")
        list_of_ratings = []
        try:
            ratings = counter.get_ratings(bad, not_special, good, very_good, excellent)
            list_of_ratings.append(ratings)
        except UnboundLocalError:
            return self.render_template("error1.html")
        text = counter.get_text(bad, not_special, good, very_good, excellent)
        average_rating_float = counter.get_average_rating_float(list_of_ratings)
        counter.add_name_information_image_average_rating_average_rating_float_in_str_to_model(name, information, image,
                                                                                           text, list_of_ratings,
                                                                                           average_rating_float)
        movies = Movies.query().fetch()
        for movie in movies:
            counter.define_number_of_ratings(movie)
        params = {"movies": movies}
        return self.render_template("add-post.html", params)


class MoviesListHandler(BaseHandler):
    def get(self):
        movies = Movies.query().fetch()
        params = {"movies": movies}
        return self.render_template("movies-list.html", params=params)


class SearchMovieHandler(BaseHandler):
    def post(self):
        search = self.request.get("search")
        text = self.request.get("text")
        date = self.request.get("date")
        rating = self.request.get("ratings")
        try:
            result_list = counter.search_and_return_result_list(search, text, date, rating)
        except:
            self.render_template("movies-list.html")
        params = {"result_list": result_list}
        return self.render_template("movies-list.html", params=params)


class MovieDetailsHandler(BaseHandler):
    def get(self, movie_id):
        movie = Movies.get_by_id(int(movie_id))
        date_created = str(movie.created)[0:10]
        time_created = str(movie.created)[11:19]
        author_list = counter.get_author_list(movie)
        counter.define_number_of_ratings(movie)
        counter.get_number_of_excellent_ratings(movie)
        counter.get_number_of_very_good_ratings(movie)
        counter.get_number_of_good_ratings(movie)
        counter.get_number_of_not_special_ratings(movie)
        counter.get_number_of_bad_ratings(movie)
        params = {"movie": movie,"date_created": date_created, "time_created": time_created, "author_list": author_list}
        return self.render_template("movie_details.html", params=params)


class RatingMovieHandler(BaseHandler):
    def post(self, movie_id):
        list_of_ratings = []
        bad = self.request.get("bad")
        not_special = self.request.get("not_special")
        good = self.request.get("good")
        very_good = self.request.get("very_good")
        excellent = self.request.get("excellent")
        movie = Movies.get_by_id(int(movie_id))
        date_created = str(movie.created)[0:10]
        time_created = str(movie.created)[11:19]
        author_list = counter.get_author_list(movie)
        movie_last_ratings = movie.average_rating_float_list
        try:
            ratings = counter.get_ratings(bad, not_special, good, very_good, excellent)
            list_of_ratings.append(ratings)
            for ratings in movie_last_ratings:
                list_of_ratings.append(ratings)
        except UnboundLocalError:
            counter.get_number_of_excellent_ratings(movie)
            counter.get_number_of_very_good_ratings(movie)
            counter.get_number_of_good_ratings(movie)
            counter.get_number_of_not_special_ratings(movie)
            counter.get_number_of_bad_ratings(movie)
            params = {"movie": movie, "date_created": date_created, "time_created": time_created,
                      "author_list": author_list}
            return self.render_template("movie_details.html", params=params)
        average_rating_str = counter.get_average_rating_str(list_of_ratings)
        average_rating_float_in_str = counter.get_average_rating_float_in_str(list_of_ratings)
        movie.average_rating_float_in_str = average_rating_float_in_str
        movie.average_rating_float_list = list_of_ratings
        movie.average_rating_str = average_rating_str
        movie.put()
        counter.define_number_of_ratings(movie)
        counter.define_number_of_ratings(movie)
        counter.get_number_of_excellent_ratings(movie)
        counter.get_number_of_very_good_ratings(movie)
        counter.get_number_of_good_ratings(movie)
        counter.get_number_of_not_special_ratings(movie)
        counter.get_number_of_bad_ratings(movie)
        params = {"movie": movie, "date_created": date_created, "time_created": time_created,
                  "author_list": author_list}
        return self.render_template("movie_details.html", params=params)


class DeleteMovieHandler(BaseHandler):
    def post(self, movie_id):
        movie = Movies.get_by_id(int(movie_id))
        try:
            movie.key.delete()
        except AttributeError:
            movies = Movies.query().fetch()
            params = {"movies": movies}
            return self.render_template("movies-list.html", params=params)
        movies = Movies.query().fetch()
        params = {"movies": movies}
        return self.render_template("movies-list.html", params=params)


class AddCommentHandler(BaseHandler):
    def post(self, movie_id):
        movie = Movies.get_by_id(int(movie_id))
        comment = self.request.get("comment")
        author = self.request.get("author")
        counter.add_movie_comment_and_movie_author(movie, comment, author)
        date_created = str(movie.created)[0:10]
        time_created = str(movie.created)[11:19]
        author_list = counter.get_author_list(movie)
        params = {"movie": movie, "date_created": date_created, "time_created": time_created,
                  "author_list": author_list}
        return self.render_template("movie_details.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainPage),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route("/movies-list", MoviesListHandler),
    webapp2.Route("/movies-list/search", SearchMovieHandler),
    webapp2.Route('/movie/<movie_id:\d+>', MovieDetailsHandler),
    webapp2.Route("/rating-movie/<movie_id:\d+>", RatingMovieHandler),
    webapp2.Route('/movie/<movie_id:\d+>/delete', DeleteMovieHandler),
    webapp2.Route("/movie/<movie_id:\d+>/comment", AddCommentHandler),
], debug=True)