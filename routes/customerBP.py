from flask import Blueprint
from controllers.customerController import save, find_all, find_customers_gmail, find_all_pagination, get_customers_orders, delete, update, find_by_id

customer_blueprint = Blueprint('customer_bp', __name__)
customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/<int:id>', methods=['PUT'])(update)
customer_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)
customer_blueprint.route('/<int:id>', methods=['DELETE'])(delete)
customer_blueprint.route('/gmail', methods=['GET'])(find_customers_gmail)
customer_blueprint.route('/paginate', methods=['GET'])(find_all_pagination)
customer_blueprint.route('/price-total', methods=['GET'])(get_customers_orders)

