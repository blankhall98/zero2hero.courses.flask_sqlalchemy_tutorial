from app.extensions import app, db

def create_app():
    
    #Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #Blueprints
    from app.routes import main, user
    app.register_blueprint(main.main)
    app.register_blueprint(user.user, url_prefix='/user')

    #Create database models
    #from app.models import User
    with app.app_context():
        db.create_all()

    return app

