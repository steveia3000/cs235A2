from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import MovieProject.adapters.repository as repo
import MovieProject.utilities.utilities as utilities
import MovieProject.movies.services as services

from MovieProject.authentication.authentication import login_required


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_date', methods=['GET'])
def movies_by_date():
    # Read query parameters.
    target_date = request.args.get('date')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_date is None:
        target_date = first_movie['date']
    else:
        # Convert target_date from string to date.
        target_date = int(target_date)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    movies, previous_date, next_date = services.get_movies_by_date(target_date, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There's at least one movie for the target date.
        if previous_date is not None:
            # There are movies on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_date', date=previous_date)
            first_movie_url = url_for('movies_bp.movies_by_date', date=first_movie['date'])

        # There are movies on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_date is not None:
            next_movie_url = url_for('movies_bp.movies_by_date', date=next_date)
            last_movie_url = url_for('movies_bp.movies_by_date', date=last_movie['date'])

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_date', date=target_date, view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title=target_date,
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    # No movies to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 3

    # Read query parameters.
    genre_name = request.args.get('genre')
    if genre_name is not None:
        cursor = request.args.get('cursor')
        movie_to_show_reviews = request.args.get('view_reviews_for')

        if movie_to_show_reviews is None:
            # No view-reviews query parameter, so set to a non-existent movie id.
            movie_to_show_reviews = -1
        else:
            # Convert movie_to_show_reviews from string to int.
            movie_to_show_reviews = int(movie_to_show_reviews)

        if cursor is None:
            # No cursor query parameter, so initialise cursor to start at the beginning.
            cursor = 0
        else:
            # Convert cursor from string to int.
            cursor = int(cursor)

        # Retrieve movie ids for movies that are genreged with genre_name.
        movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)

        # Retrieve the batch of movies to display on the Web page.
        movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

        first_movie_url = None
        last_movie_url = None
        next_movie_url = None
        prev_movie_url = None

        if cursor > 0:
            # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
            first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

        if cursor + movies_per_page < len(movie_ids):
            # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
            next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

            last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
            if len(movie_ids) % movies_per_page == 0:
                last_cursor -= movies_per_page
            last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor, view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title=genre_name + " movies",
            movies_title= genre_name + " movies",
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    else:
        return render_template(
            'movies/movies.html',
            title='movie categories',
            movies=None,
            search=False,
            selected_movies=utilities.get_selected_movies(4),
            genres_urls=utilities.get_genres_and_urls(),
        )




@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie id, when subsequently called with a HTTP POST request, the movie id remains in the
    # form.
    form = reviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new review.
        services.add_review(movie_id, form.review.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same date as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movies_bp.movies_by_date', date=movie['date'], view_reviews_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie id of the movie being reviewed from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/review_on_movie.html',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class reviewForm(FlaskForm):
    review = TextAreaField('review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_id = HiddenField("movie id")
    submit = SubmitField('Submit')