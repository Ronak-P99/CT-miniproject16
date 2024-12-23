from flask import Blueprint
from controllers.productionController import save, find_all, get_production_dates, update, find_by_id, delete

production_blueprint = Blueprint('production_bp', __name__)
production_blueprint.route('/', methods=['POST'])(save)
production_blueprint.route('/', methods=['GET'])(find_all)
production_blueprint.route('/quantity-dates', methods=['GET'])(get_production_dates)
production_blueprint.route('/<int:id>', methods=['PUT'])(update)
production_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)
production_blueprint.route('/<int:id>', methods=['DELETE'])(delete)