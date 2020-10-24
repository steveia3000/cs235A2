import csv
import os
from typing import List
from bisect import bisect_left, insort_left
from werkzeug.security import generate_password_hash
from MovieProject.adapters.repository import AbstractRepository, RepositoryException
from MovieProject.domain.model import User, Movie, Genre, make_review, make_genre_association, ModelException, Review, \
    Director, Actor


class MemoryRepository(AbstractRepository):
    # movies ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.directors = list()
        self.actors = list()
        self._movies = list()
        self._movies_index = dict()
        self._genres = list()
        self._users = list()
        self._reviews = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movies_by_date(self, target_date: int) -> List[Movie]:
        target_movie = Movie("a", target_date)
        matching_movies = list()

        try:
            index = self.movie_index(target_movie)
            for movie in self._movies[index:None]:
                if movie.release_year == target_date:
                    matching_movies.append(movie)
                else:
                    break
        except ValueError:
            # No movies for specified date. Simply return an empty list.
            pass

        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent movie ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a genre with the name genre_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of movies associated with the genre.
        if genre is not None:
            movie_ids = [movie.id for movie in genre.movies]
        else:
            # No genre with name genre_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    def get_date_of_previous_movie(self, movie: Movie):
        previous_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release_year < movie.release_year:
                    previous_date = stored_movie.release_year
                    break
        except ValueError:
            # No earlier movies, so return None.
            pass

        return previous_date

    def get_date_of_next_movie(self, movie: Movie):
        next_date = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release_year > movie.release_year:
                    next_date = stored_movie.release_year
                    break
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return next_date

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_year == movie.release_year:
            return index
        raise ValueError

    def movies_index(self):
        return self._movies_index

    def get_genre(self, genre_name):
        return next((genre for genre in self._genres if genre.genre_name == genre_name), None)

    def get_movies_by_actor(self, name):
        actor = next((actor for actor in self.actors if actor.actor_full_name == name), None)

        # Retrieve the ids of movies associated with the genre.
        if actor:
            print(actor.movies)
            return actor.movies
        return []

    def get_movies_by_director(self,director_name):
        director = next((director for director in self.directors if director.director_full_name == director_name), None)
        print(director)
        # Retrieve the ids of movies associated with the genre.
        if director:
            print(director)
            print(director.movies)
            return director.movies
        return []

    def get_actor(self, actor_name):
        return next((actor for actor in self.actors if actor.actor_full_name == actor_name), None)

    def get_director(self, d):
        return next((director for director in self.directors if director.director_full_name == d), None)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_genres(data_path: str, repo: MemoryRepository):

    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):

        movie_id = int(data_row[0])
        movie_genres = data_row[2].split(",")
        movie_actor = data_row[5].split(",")
        movie_director = data_row[4]
        movie_title = data_row[1]
        movie_description = data_row[3]
        movie_runtime = int(data_row[7])
        movie_release_year = int(data_row[6])
        movie_metascore = data_row[-1]
        movie_rating = data_row[8]

        # Create movie object.
        movie = Movie(movie_title, movie_release_year)
        movie.id = movie_id
        movie.description = movie_description
        movie.runtime_minutes = movie_runtime
        movie.metascore = movie_metascore
        movie.rating = movie_rating


        # Add any new genres; associate the current movie with genres.
        for genre_name in movie_genres:
            genre = repo.get_genre(genre_name)
            if genre is None:
                genre = Genre(genre_name)
            make_genre_association(movie, genre)
            movie.add_genre(genre)
            repo.add_genre(genre)

        for actor_name in movie_actor:
            actor = repo.get_actor(actor_name)
            if actor is None:
                actor = Actor(actor_name)
                repo.actors.append(actor)
            movie.add_actor(actor)
            actor.movies.append(movie)

        director = repo.get_director(movie_director)
        if director is None:
            director = Director(movie_director)
            repo.directors.append(director)
        movie.director = director
        movie.director.movies.append(movie)

        # Add the movie to the repository.
        repo.add_movie(movie)

def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            time=data_row[4]
        )
        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies and genres into the repository.
    load_movies_and_genres(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
