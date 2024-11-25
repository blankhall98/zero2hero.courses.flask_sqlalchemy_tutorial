from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/get/<int:id>')
def get_user(id):
    return f'User {id}'