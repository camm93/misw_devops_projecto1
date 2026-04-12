from datetime import datetime

from app.extensions import db


class Blacklist(db.Model):

    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), nullable=False, index=True)

    app_uuid = db.Column(db.String(36), nullable=False, index=True)

    blocked_reason = db.Column(db.String(255))

    ip_address = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (db.UniqueConstraint("email", "app_uuid", name="uq_email_app"),)
