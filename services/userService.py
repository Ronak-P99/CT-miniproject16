from models.user import User
from database import db
from utils.util import encode_token
from werkzeug.security import check_password_hash


def login_customer(username, password):
    user = (db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none())
    role_names = [role.role_name for role in user.roles]
    if user:
        if check_password_hash(user.password, password):    
            auth_token = encode_token(user.id, role_names)
            resp = {
                "status": "success",
                "message": "Successfully logged in",
                "auth_token": auth_token
            }
            return resp
        else:
            return None
    else:
        return None