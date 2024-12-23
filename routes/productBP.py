from flask import Blueprint
from controllers.productController import save, find_all_pagination, find_all, get_max_orders, update, find_by_id, delete

product_blueprint = Blueprint('product_bp', __name__)
product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/paginate', methods=['GET'])(find_all_pagination)
product_blueprint.route('/', methods=['GET'])(find_all)
product_blueprint.route('/product-max', methods=['GET'])(get_max_orders)
product_blueprint.route('/<int:id>', methods=['PUT'])(update)
product_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)
product_blueprint.route('/<int:id>', methods=['DELETE'])(delete)
