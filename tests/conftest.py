import os
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")

from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    return app


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    return app.test_client()


@pytest.fixture(scope="session")
def auth_headers():
    return {"Authorization": "Bearer test-secret"}
