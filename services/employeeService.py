from sqlalchemy.orm import Session
from database import db
from models.employee import Employee
from circuitbreaker import circuit
from sqlalchemy import select, func
from models.production import Production
from models.product import Product

def fallback_function(employee):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(employee_data):
    try:
        if employee_data['name'] == "Failure":
            raise Exception("Failure condition triggered")
        
        with Session(db.engine) as session:
            with session.begin():
                new_employee = Employee(name=employee_data['name'], position=employee_data['position'])
                session.add(new_employee)
                session.commit() 
            session.refresh(new_employee)
            return new_employee
        # Create a new static function
    except Exception as e:
           raise e
    
def find_by_id(id):
    query = select(Employee).where(Employee.id == id)
    employee = db.session.execute(query).scalar_one_or_none()
    return employee

def update(id, employee_data):
    employee = find_by_id(id)
           
    if not employee:
        raise ValueError(f"employee with ID {id} does not exist")

    employee.name = employee_data['name']
    employee.position = employee_data['position']
    
    db.session.commit()

    return employee

def delete(id):
    employee = find_by_id(id)
           
    if not employee:
        raise ValueError(f"employee with ID {id} does not exist")
    
    db.session.delete(employee)
    db.session.commit()

    return "Successfully deleted"

def find_all():
    query = select(Employee)
    employees = db.session.execute(query).scalars().all()
    return employees

def get_production():
   # Query to calculate total production per employee
    results = db.session.query(
        Employee.name,
        func.sum(Production.quantity_produced).label('total_quantity')
    ).join(Production, Employee.id == Production.employee_id).join(Product, Production.product_id == Product.id) \
    .group_by(Employee.name).all()
    return [{'employee_name': name, 'total_quantity': total} for name, total in results]

# def get_max_production():
#    # Query to calculate total production per employee
#     max_value = float('-inf')    
#     results = db.session.query(
#         Employee.name,
#         func.sum(Production.quantity_produced).label('total_quantity')
#     ).join(Production, Employee.id == Production.employee_id).join(Product, Production.product_id == Product.id) \
#     .group_by(Product.name).all()
#     for name, total in results:
#         if total > max_value:
#             max_value = total
#             max_name = name

#     return {'employee_name': max_name, 'total_quantity': max_value} 