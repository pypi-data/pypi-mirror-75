from werkzeug.exceptions import abort

from ..app import DB
from ..models.user import User, UserSchema


def get_users_list():
    users = User.query.order_by(User.id).all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)


def get_user(email):
    user = User.query.filter(User.email == email).one_or_none()
    if not user:
        abort(404, "No user exists for provided email.")

    user_schema = UserSchema()
    data = user_schema.dump(user)

    return data


def add_user(body):
    user_email = body.get("email")
    user = User.query.filter_by(email=user_email).one_or_none()
    if user:
        abort(409, "User with same email already exists.")

    user = User(email=user_email)
    DB.session.add(user)
    DB.session.commit()

    user_schema = UserSchema()
    d_user = user_schema.dump(user)

    return d_user, 201
