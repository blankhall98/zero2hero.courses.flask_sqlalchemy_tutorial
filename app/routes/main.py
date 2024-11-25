from flask import Blueprint, request, render_template, redirect, url_for
from app.extensions import db
from app.models.user import User
from app.models.item import Item
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

### CRUD Operations ###

#create - user
@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        #recolectar los datos del formulario
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        #¿ya existe el usuario?
        # FROM User SELECT * WHERE username = username LIMIT 1
        user = User.query.filter_by(username=username).first()
        if user:
            return 'nombre de usuario ya existe'
        
        #hash de la contraseña
        password = generate_password_hash(password)

        #insertar en base de datos
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')

#read
@main.route('/get_users')
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/get_user_by_id', methods=['GET', 'POST'])
def get_user_by_id():
    if request.method == 'POST':
        id = request.form['id']
        user = User.query.get(id)
        if user:
            return f'{user.username} - {user.email} - {user.password}'
        else:
            return 'usuario no existe'
        
@main.route('/get_user_by_username', methods=['GET', 'POST'])
def get_user_by_username():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            return f'{user.username} - {user.email} - {user.password}'
        else:
            return 'usuario no existe'
    else:
        return f'{request.method}'

#update
@main.route('/update_user_by_id', methods=['GET', 'POST'])
def update_user_by_id():
    if request.method == 'POST':
        id = request.form['id']
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        new_email = request.form['new_email']

        user = User.query.get(id)
        if user:
            user.username = new_username
            user.password = generate_password_hash(new_password)
            user.email = new_email
            db.session.commit()
            return 'usuario actualizado'
        else:
            return 'usuario no existe'


@main.route('/update_user_by_username', methods=['GET', 'POST'])
def update_user_by_username():
    if request.method == 'POST':
        username = request.form['username']
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        new_email = request.form['new_email']
        
        user = User.query.filter_by(username=username).first()
        if user:
            user.username = new_username
            user.password = generate_password_hash(new_password)
            user.email = new_email
            db.session.commit()
            return 'usuario actualizado'
        else:
            return 'usuario no existe'


#delete
@main.route('/delete_user_by_id', methods=['GET', 'POST'])
def delete_user_by_id():
    if request.method == 'POST':
        id = request.form['id']
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return 'usuario eliminado'
        else:
            return 'usuario no existe'
        
@main.route('/delete_user_by_username', methods=['GET', 'POST'])
def delete_user_by_username():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return 'usuario eliminado'
        else:
            return 'usuario no existe'

#validate
@main.route('/validate', methods=['GET', 'POST'])
def validate_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #buscar el usuario
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'usuario validado'
            else:
                return 'contraseña incorrecta'
        else:
            return 'usuario no existe'
    else:
        return render_template('validate.html')
    
#create item
@main.route('/create_item', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id = request.form['user_id']

        new_item = Item(name=name, description=description, user_id=user_id)
        db.session.add(new_item)
        db.session.commit()

        return 'item creado'
    else:
        return render_template('create_item.html')
    

@main.route('/get_items_by_user_id', methods=['GET', 'POST'])
def get_items_by_user_id():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_info = User.query.get(user_id)
        if user_info:
            items = Item.query.filter_by(user_id=user_id).all()
            if items:
                return render_template('show_items.html', items=items, user_info=user_info)
            else:
                return 'no hay items'
        else:
            return 'usuario no existe'

