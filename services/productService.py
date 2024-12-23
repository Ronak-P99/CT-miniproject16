from sqlalchemy.orm import Session
from database import db
from models.product import Product
from sqlalchemy import select, func
from models.order import Order

def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            order_id = product_data['order_id']
            order = session.execute(select(Order).where(Order.id == order_id)).scalars().first()
           
            if not order:
                raise ValueError(f"Customer with ID {order_id} does not exist")
            
            new_product = Product(name=product_data['name'], price=product_data['price'], quantity_ordered=product_data['quantity_ordered'], order_id=product_data['order_id'])
            session.add(new_product)
            print("New Product ID (before commit):", new_product.id)
            session.flush()
            print("New Product ID (after commit):", new_product.id)
            session.commit() 
        session.refresh(new_product)
        return new_product

def find_by_id(id):
    query = select(Product).join(Order).where(Order.id == Product.order_id).filter_by(id=id)
    product = db.session.execute(query).scalar_one_or_none()
    return product

def update(id, product_data):
    product = find_by_id(id)
           
    if not product:
        raise ValueError(f"Product with ID {id} does not exist")

    product.name = product_data['name']
    product.price = product_data['price']
    product.quantity_ordered = product_data['quantity_ordered']
    
    
    db.session.commit()

    return product

def delete(id):
    product = find_by_id(id)
           
    if not product:
        raise ValueError(f"Product with ID {id} does not exist")
    
    db.session.delete(product)
    db.session.commit()

    return "Successfully deleted"
        
def find_all_pagination(page=1, per_page=10):
    products = db.paginate(select(Product), page=page, per_page=per_page)
    return products

def find_all():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products

def get_max_orders():
   # Query to calculate total production per employee
    results = db.session.query(
        Product.name,
        func.sum(Product.quantity_ordered).label('total_quantity_ordered')
    ).join(Order, Order.id == Product.order_id) \
    .group_by(Product.name).order_by(func.sum(Product.quantity_ordered).desc()).all()

    return [{'product_name': name, 'total_quantity_ordered': total} for name, total in results]
