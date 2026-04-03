from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Blacklist


def add_email_to_blacklist(email, app_uuid, blocked_reason, ip_address):
    blacklist_entry = Blacklist(
        email=email.strip().lower(),
        app_uuid=app_uuid,
        blocked_reason=blocked_reason,
        ip_address=ip_address,
    )

    try:
        db.session.add(blacklist_entry)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None

    return blacklist_entry


def check_email_blacklist(email):
    normalized_email = email.strip().lower()

    entry = Blacklist.query.filter_by(email=normalized_email).first()

    if entry:
        return True, entry.blocked_reason

    return False, None