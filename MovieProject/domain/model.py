from datetime import datetime


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

        self.movies = list()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f'{self.__director_full_name}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.director_full_name == self.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
        self.__movies = []

    @property
    def movies(self):
        return self.__movies

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name == self.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)

    def is_applied_to(self, movie):
        return movie in self.__movies

    def add_movie(self, movie):
        self.__movies.append(movie)


class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

        self.__actors_this_one_has_worked_with = set()
        self.movies = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, self.__class__):
            self.__actors_this_one_has_worked_with.add(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__actors_this_one_has_worked_with

    def __repr__(self):
        return f'{self.__actor_full_name}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)


class Movie:

    def __set_title_internal(self, title: str):
        if title.strip() == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

    def __set_release_year_internal(self, release_year: int):
        if release_year >= 1900 and type(release_year) is int:
            self.__release_year = release_year
        else:
            self.__release_year = None

    def __init__(self, title: str, release_year: int):

        self.__rating = None
        self.__set_title_internal(title)
        self.__set_release_year_internal(release_year)

        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__reviews = []
        self.__id = None
        self.__metascore = None

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, Id: int):
        if type(Id) is int:
            self.__id = Id

    @property
    def reviews(self):
        return self.__reviews

    @property
    def metascore(self):
        return self.__metascore

    @metascore.setter
    def metascore(self, score):
        self.__metascore = score

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, r):
        self.__rating = r



    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__set_title_internal(title)

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        self.__set_release_year_internal(release_year)

    # additional attributes

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if type(description) is str:
            self.__description = description.strip()
        else:
            self.__description = None

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, director: Director):
        if isinstance(director, Director):
            self.__director = director
        else:
            self.__director = None

    @property
    def actors(self) -> list:
        return self.__actors

    def add_actor(self, actor: Actor):
        if not isinstance(actor, Actor) or actor in self.__actors:
            return

        self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if not isinstance(actor, Actor):
            return

        try:
            self.__actors.remove(actor)
        except ValueError:
            # print(f"Movie.remove_actor: Could not find {actor} in list of actors.")
            pass

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return

        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return

        try:
            self.__genres.remove(genre)
        except ValueError:
            # print(f"Movie.remove_genre: Could not find {genre} in list of genres.")
            pass

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, val: int):
        if val > 0:
            self.__runtime_minutes = val
        else:
            raise ValueError(f'Movie.runtime_minutes setter: Value out of range {val}')

    def __get_unique_string_rep(self):
        return f"{self.__title}, {self.__release_year}"

    def __repr__(self):
        return f'<Movie {self.__get_unique_string_rep()}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__get_unique_string_rep() == other.__get_unique_string_rep()

    def __lt__(self, other):
        if self.title == other.title:
            return self.release_year < other.release_year
        return self.release_year < other.release_year

    def __hash__(self):
        return hash(self.__get_unique_string_rep())

    def add_review(self, review):
        self.__reviews.append(review)

    @property
    def number_of_reviews(self):
        return len(self.__reviews)

    @property
    def number_of_genres(self):
        return len(self.__genres)

    def is_genre(self):
        return self.__genres

    def is_genre_by(self, g):
        return g in self.__genres


class Review:

    def __init__(self, user, movie: Movie, review_text: str):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None
        if type(review_text) is str:
            self.__review_text = review_text
        else:
            self.__review_text = None

        self.__rating = None
        if type(user) is  User:
            self.__author = user
        else:
            self.__author = None
        self.__timestamp = datetime.now()

    @property
    def author(self):
        return self.__author

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.movie == self.__movie and other.review_text == self.__review_text and other.rating == self.__rating and other.timestamp == self.__timestamp

    def __repr__(self):
        return f'<Review of movie {self.__movie}, rating = {self.__rating}, timestamp = {self.__timestamp}>'

    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def username(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.__user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.username == self.__user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)


class ModelException(Exception):
    pass


def make_review(review_text: str, user: User, movie: Movie, time):
    review = Review(user, movie, review_text)
    user.add_review(review)
    movie.add_review(review)
    if time is not None:
        review.timestamp = time
    return review


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'genre {genre.genre_name} already applied to movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)

