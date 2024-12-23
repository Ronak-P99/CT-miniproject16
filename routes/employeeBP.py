from flask import Blueprint
from controllers.employeeController import save, find_all, get_production, update, find_by_id, delete

employee_blueprint = Blueprint('employee_bp', __name__)
employee_blueprint.route('/', methods=['POST'])(save)
employee_blueprint.route('/', methods=['GET'])(find_all)
employee_blueprint.route('/<int:id>', methods=['PUT'])(update)
employee_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)
employee_blueprint.route('/<int:id>', methods=['DELETE'])(delete)
employee_blueprint.route('/production-report', methods=['GET'])(get_production)
