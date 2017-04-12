from models import Movies


def get_average_rating_str(list_of_ratings):
    float_in_list_of_ratings = [num for num in list_of_ratings if isinstance(num, (int, float))]
    if len(float_in_list_of_ratings) > 0:
        average = sum(float_in_list_of_ratings) / float(len(float_in_list_of_ratings))
        if average < 1.5:
            average = "bad"
        elif average < 2.5:
            average = "not special"
        elif average < 3.5:
            average = "good"
        elif average < 4.5:
            average = "very good"
        elif average > 4.5 or average == 4.5:
            average = "excellent"
    else:
        average = None
    return average

def get_average_rating_float(list_of_ratings):
    float_in_list_of_ratings = [num for num in list_of_ratings if isinstance(num, (int, float))]
    if len(float_in_list_of_ratings) > 0:
        average_rating_float = sum(float_in_list_of_ratings) / float(len(float_in_list_of_ratings))
        return average_rating_float
    else:
        return None

def get_average_rating_float_in_str(list_of_ratings):
    float_in_list_of_ratings = [num for num in list_of_ratings if isinstance(num, (int, float))]
    if len(float_in_list_of_ratings) > 0:
        average_rating_float = sum(float_in_list_of_ratings) / float(len(float_in_list_of_ratings))
        average_rating_float_in_str = str(average_rating_float)[:3]
        return average_rating_float_in_str
    else:
        return None


def define_number_of_ratings(movie):
    average_rating_float_list = movie.average_rating_float_list
    number_of_ratings = len(average_rating_float_list)
    movie.number_of_ratings = str(number_of_ratings)
    movie.put()


def add_movie_comment_and_movie_author(movie, comment, author):
    list_of_comments = []
    list_of_authors = []
    comment = str(comment)
    author = str(author)
    list_of_comments.append(comment)
    if author:
        list_of_authors.append(author)
    if not author:
        list_of_authors.append("Anonymous")
    get_last_comments = movie.comments
    for comments in get_last_comments:
        list_of_comments.append(comments)
    movie.comments = list_of_comments
    get_last_authors = movie.author
    for authors in get_last_authors:
        list_of_authors.append(authors)
    movie.author = list_of_authors
    movie.put()


def get_author_list(movie):
    author_list = []
    get_last_authors = movie.author
    for authors in get_last_authors:
        author_list.append(authors)
    return  author_list


def search_and_return_result_list(search, text, date, rating):
    result_list = []
    movies = Movies.query().fetch()
    search = search.lower()
    if text:
        for movie in movies:
            index_position = movie.name.lower().find(search)
            if index_position > -1:
                result_list.append(movie)
    if date:
        for movie in movies:
            date = str(movie.created)[0:10]
            index_position = date.find(search)
            if index_position > -1:
                result_list.append(movie)
    if rating:
        for movie in movies:
            rating_str = movie.average_rating_str
            index_position = rating_str.find(search)
            if index_position > -1:
                result_list.append(movie)
        for movie in movies:
            rating_number = movie.average_rating_float_in_str
            index_position = rating_number.find(search)
            if index_position > -1:
                result_list.append(movie)
    return result_list


def get_ratings(bad, not_special, good, very_good, excellent):
    if bad:
        ratings = 1.0
    if not_special:
        ratings = 2.0
    if good:
        ratings = 3.0
    if very_good:
        ratings = 4.0
    if excellent:
        ratings = 5.0
    return ratings


def get_text(bad, not_special, good, very_good, excellent):
    if bad:
        text = "bad"
    if not_special:
        text = "not special"
    if good:
        text = "good"
    if very_good:
        text = "very good"
    if excellent:
        text = "excellent"
    return text


def add_name_information_image_average_rating_average_rating_float_in_str_to_model(name, information, image, text, list_of_ratings,  average_rating_float):
    if not information:
        information = "..."
    if not image:
        image = "http://www.androidcrush.com/wp-content/uploads//2016/03/best-Free-movie-apps-for-android-2016.jpg"
    average_rating_float_in_str = str(average_rating_float)[:3]
    msg_object = Movies(name=name,
                        information=information.replace("<script>", ""), image=image,
                        average_rating_str=text, average_rating_float_list=list_of_ratings,
                        average_rating_float_in_str=average_rating_float_in_str)  # another way to fight JS injection
    msg_object.put()


def add_average_ratung_float_in_str_to_model(movie, average_rating_float):
    average_rating_float_in_str = str(average_rating_float)[:3]
    movie.average_rating_float_in_str = average_rating_float_in_str
    movie.put()

def get_number_of_excellent_ratings(movie):
    list_of_excellent_ratings = []
    movie_ratings = movie.average_rating_float_list
    for rating in movie_ratings:
         if rating == 5.0:
            list_of_excellent_ratings.append(rating)
    number_of_excellent_ratings = len(list_of_excellent_ratings)
    number_of_excellent_ratings_str = str(number_of_excellent_ratings)
    movie.number_of_excellent_ratings_str = number_of_excellent_ratings_str

def get_number_of_very_good_ratings(movie):
    list_of_very_good_ratings = []
    movie_ratings = movie.average_rating_float_list
    for rating in movie_ratings:
         if rating == 4.0:
            list_of_very_good_ratings.append(rating)
    number_of_very_good_ratings = len(list_of_very_good_ratings)
    number_of_very_good_ratings_str = str(number_of_very_good_ratings)
    movie.number_of_very_good_ratings_str = number_of_very_good_ratings_str

def get_number_of_good_ratings(movie):
    list_of_good_ratings = []
    movie_ratings = movie.average_rating_float_list
    for rating in movie_ratings:
         if rating == 3.0:
            list_of_good_ratings.append(rating)
    number_of_good_ratings = len(list_of_good_ratings)
    number_of_good_ratings_str = str(number_of_good_ratings)
    movie.number_of_good_ratings_str = number_of_good_ratings_str


def get_number_of_not_special_ratings(movie):
    list_of_not_special_ratings = []
    movie_ratings = movie.average_rating_float_list
    for rating in movie_ratings:
        if rating == 2.0:
            list_of_not_special_ratings.append(rating)
    number_of_not_special_ratings = len(list_of_not_special_ratings)
    number_of_not_special_ratings_str = str(number_of_not_special_ratings)
    movie.number_of_not_special_ratings_str = number_of_not_special_ratings_str

def get_number_of_bad_ratings(movie):
    list_of_bad_ratings = []
    movie_ratings = movie.average_rating_float_list
    for rating in movie_ratings:
        if rating == 1.0:
            list_of_bad_ratings.append(rating)
    number_of_bad_ratings = len(list_of_bad_ratings)
    number_of_bad_ratings_str = str(number_of_bad_ratings)
    movie.number_of_bad_ratings_str = number_of_bad_ratings_str

