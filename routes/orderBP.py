from flask import Blueprint
from controllers.orderController import save, find_by_id, find_all_pagination, find_all, update, delete

order_blueprint = Blueprint('order_bp', __name__)
order_blueprint.route('/', methods=['POST'])(save)
order_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)
order_blueprint.route('/<int:id>', methods=['PUT'])(update)
order_blueprint.route('/<int:id>', methods=['DELETE'])(delete)
order_blueprint.route('/paginate', methods=['GET'])(find_all_pagination)
order_blueprint.route('/', methods=['GET'])(find_all)
