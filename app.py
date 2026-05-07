from flask import Flask, jsonify
from flask_migrate import Migrate
from flasgger import Swagger

from Data import db, jwt
from Data.db import jwt_blocklist
from werkzeug.security import generate_password_hash
from Controllers import auth_bp, user_bp, bike_bp, rental_bp
from Models.user import User


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blocklist



def ensure_single_admin():
    admin = User.query.filter_by(username="admin").first()

    if not admin:
        admin = User(
            username="admin",
            password=generate_password_hash("Admin@123"),
            name="System Admin",
            age=30,
            role="ADMIN"
        )
        db.session.add(admin)
        db.session.commit()



def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "bike-rental-api-jwt-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql+psycopg2://postgres:Postgres@localhost:5432/bike_rental_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db) 


    with app.app_context():
        ensure_single_admin()

    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Bike Rental API",
            "description": "Bike Rental Management System API",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header. Example: Bearer <token>"
            }
        },
        
        "security": [
            { "Bearer": [] }
        ]

    })

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(bike_bp, url_prefix="/api/bikes")
    app.register_blueprint(rental_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return jsonify({"message": "Bike Rental API is running"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)