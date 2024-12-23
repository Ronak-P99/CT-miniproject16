from flask import Blueprint
from controllers.customerAccountController import find_all, save, update, delete, find_by_id, login

customer_account_blueprint = Blueprint('customer_account_bp', __name__)
customer_account_blueprint.route('/', methods=['POST'])(save)
customer_account_blueprint.route('/', methods=['GET'])(find_all)
customer_account_blueprint.route('/<int:id>', methods=['PUT'])(update)
customer_account_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)
customer_account_blueprint.route('/<int:id>', methods=['DELETE'])(delete)
customer_account_blueprint.route('/login', methods=['POST'])(login)