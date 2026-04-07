import os

from flask import Flask, jsonify
from flask_restful import Api

from app.config import Config
from app.extensions import db, ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    api = Api(app)

    from app.resources import BlacklistCheckResource, BlacklistResource

    api.add_resource(BlacklistResource, "/blacklists")
    api.add_resource(BlacklistCheckResource, "/blacklists/<string:email>")

    @app.route("/")
    def health_check():
        return jsonify({
            "status": "ok",
            "version": os.environ.get("APP_VERSION", "1.0"),
        }), 200

    with app.app_context():
        db.create_all()

    return app
