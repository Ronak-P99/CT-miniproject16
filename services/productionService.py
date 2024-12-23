from sqlalchemy.orm import Session
from database import db
from models.production import Production
from circuitbreaker import circuit
from sqlalchemy import select, func
from models.product import Product
from models.employee import Employee

def fallback_function(production):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(production_data):
    try:
        if production_data['name'] == "Failure":
            raise Exception("Failure condition triggered")
        
        with Session(db.engine) as session:
            with session.begin():
                new_production = Production(name=production_data['name'], quantity_produced=production_data['quantity_produced'], product_id=production_data['product_id'], employee_id=production_data['employee_id'], date=production_data['date'])
                session.add(new_production)
                session.commit() 
            session.refresh(new_production)
            return new_production
        
    except Exception as e:
           raise e
    
def find_by_id(id):
    query = select(Production).join(Product).join(Employee).where(Product.id == Production.product_id and Employee.id == Production.employee_id).filter_by(id=id)
    production = db.session.execute(query).scalar_one_or_none()
    return production

def update(id, production_data):
    production = find_by_id(id)
           
    if not production:
        raise ValueError(f"Production with ID {id} does not exist")

    production.name = production_data['name']
    production.quantity_produced = production_data['quantity_produced']
    production.date = production_data['date']

    
    
    db.session.commit()

    return production

def delete(id):
    production = find_by_id(id)
           
    if not production:
        raise ValueError(f"Production with ID {id} does not exist")
    
    db.session.delete(production)
    db.session.commit()

    return "Successfully deleted"

def find_all():
    query = select(Production)
    productions = db.session.execute(query).scalars().all()
    return productions

def get_production_dates():
    results = db.session.query(
        Product.name,
        func.sum(Product.quantity_ordered).label('quantity_ordered')
    ).select_from(Production) \
    .join(Product, Product.id == Production.product_id) \
    .filter(Production.date > "1234-11-10") \
    .group_by(Product.name) \
    .all()

    return [{'product_name': name, 'quantity_ordered': total} for name, total in results]