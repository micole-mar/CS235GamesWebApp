from flask import Blueprint, render_template, request
import games.adapters.repository as repo
import games.search.services as services

search_blueprint = Blueprint('search_bp', __name__)

@search_blueprint.route('/search', methods=['GET', 'POST'])
def search_results():
    search_query = request.args.get('q')
    search_type = request.args.get('search_type')

    search_results = services.search_by_type(repo.repo_instance, search_query, search_type)
    return render_template(
        'search_results.html',
        title='Search Results',
        search_query=search_query,
        search_type=search_type,
        results=search_results
    )
