from datetime import datetime
from typing import List

import pytest

from MovieProject.adapters.repository import RepositoryException
from MovieProject.authentication.services import AuthenticationException
from MovieProject.domain.model import User, Movie, Genre, Review, make_review


def test_repository_can_add_a_user(in_memory_repo):
    user = User('eveFeng', '123')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('evefeng') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    assert user == User('thorke', 'cLQ^C#oFXloS')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('abc')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()
    assert number_of_movies == 4


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Funny", 2006)
    movie.id = 5
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(5) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the movie is reviewed as expected.
    review = [review for review in movie.reviews if review.review_text== 'Oh no, COVID-19 has hit New Zealand'][0]
    assert review.author.username == "fmercury"


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1000000)
    assert movie is None


def test_repository_can_retrieve_movies_by_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(2016)

    # Check that the query returned  movies.
    assert len(movies) == 2


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(1993)
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 11

    assert Genre("Action") in genres
    assert Genre("Mystery") in genres
    assert Genre("Family") in genres
    assert Genre("Sport") not in genres


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Prometheus'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Split'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([1,2,3])

    assert len(movies) == 3
    assert movies[0].title == 'Guardians of the Galaxy'
    assert movies[1].title == "Prometheus"
    assert movies[2].title == "Split"


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([1, 51,100,0])

    assert len(movies) == 1
    assert movies[0].title == 'Guardians of the Galaxy'




def test_repository_returns_movie_ranks_for_existing_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('Comedy')

    assert movie_ids == [4]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ids_for_genre('Sport')

    assert len(movie_ranks) == 0


def test_repository_returns_date_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date == 2012


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date is None


def test_repository_returns_date_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date == 2014


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Sport')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 3


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('mjackson')
    movie = in_memory_repo.get_movie(2)
    review = make_review("interesting, I recommend this movie to watch!!!", user,movie, datetime.now())
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    review = Review(None, movie, "interesting, I recommend this movie to watch!!!",)

    with pytest.raises(RepositoryException): in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('mjackson')
    movie = in_memory_repo.get_movie(10000000)
    review = Review(user, None, "interesting, I recommend this movie to watch!!!")

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the movie doesn't refer to the review.
        in_memory_repo.add_review(review)

