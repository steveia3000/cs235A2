from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import MovieProject.adapters.repository as repo

import MovieProject.utilities.utilities as utilities
from MovieProject.movies import services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    form = Search()
    return render_template(
        'home/home.html',
        form=form,
        handler_url=url_for('home_bp.search'),
        selected_movies=utilities.get_selected_movies(),
        genres_urls=utilities.get_genres_and_urls()
    )


@home_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = Search()
    search_result = None

    if form.validate_on_submit():
        search_detial = form.content.data
        return redirect(url_for('home_bp.search', search=search_detial))

    if request.method == 'GET':
        search_result = services.search_movie_by_actor(repo.repo_instance, request.args.get('search'))

    # For a GET or a failed POST request
    if not search_result:
        search_result = services.search_movie_by_director(repo.repo_instance, request.args.get('search'))

    return render_template(
        'movies/movies.html',
        movies=search_result,
        title="Search result",
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        search=True
    )


class Search(FlaskForm):
    content = StringField("content", [DataRequired()])
    submit = SubmitField("search")
