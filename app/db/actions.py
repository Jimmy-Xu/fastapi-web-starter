import logging
from typing import Callable, Iterator, Optional
from fastapi.openapi.models import APIKey
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from app.db import get_session
from app.db.models import ApiKey, Post, User
from app.library.helpers import mask_text
from app.models import api_keys
from app.security import hash_password, verify_password, manager

from typing import Tuple


@manager.user_loader(session_provider=get_session)
def get_user_by_name(
    name: str,
    db: Optional[Session] = None,
    session_provider: Callable[[], Iterator[Session]] = None
) -> Optional[User]:
    """
    Queries the database for a user with the given name

    Args:
        name: The name of the user
        db: The currently active database session
        session_provider: Optional method to retrieve a session if db is None (provided by our LoginManager)

    Returns:
        The user object or none
    """

    if db is None and session_provider is None:
        raise ValueError("db and session_provider cannot both be None.")

    if db is None:
        db = next(session_provider())

    user = db.query(User).where(User.username == name).first()
    return user


def create_user(name: str, password: str, db: Session, is_admin: bool = False) -> User:
    """
    Creates and commits a new user object to the database

    Args:
        name: The name of the user
        password: The plaintext password
        db: The active db session
        is_admin: Whether the user is a admin, defaults to false

    Returns:
        The newly created user.
    """
    hashed_pw = hash_password(password)
    user = User(username=name, password=hashed_pw, is_admin=is_admin)
    db.add(user)
    db.commit()
    return user


def reset_user_pwd(name: str, old_password: str, new_password: str, db: Session):
    """
    update user password and commits a user object to the database

    Args:
        name: The name of the user
        password: The plaintext password
        db: The active db session

    Returns:
        The updated user.
    """
    try:
        user = db.query(User).filter_by(username=name).first()
        if verify_password(old_password, user.password):
            new_hashed_pw = hash_password(new_password)
            user.password = new_hashed_pw
            db.commit()
            logging.info("reset password for user:{0} OK".format(name))
            return True, ""
        else:
            logging.error(
                "failed to reset password for user:{0}, error: current password is wrong".format(name))
            return False, "current password is wrong"
    except Exception as e:
        logging.error(
            "failed to reset password for user:{0}, error:{1}".format(name, str(e)))
        return False, "internal server error"


def create_post(text: str, owner: User, db: Session) -> Post:
    post = Post(text=text, owner=owner)

    '''
    db.add(local_object)
    db.commit()
    '''

    # https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session
    local_object = db.merge(post)
    db.add(local_object)
    db.commit()

    return post


def create_api_key(app_name: str, api_key: str, secret_key: str, owner: User, db: Session) -> Tuple[APIKey, str]:
    logging.info("create_api_key: app_name={0} api_key={1} secret_key(cipher)={2} owner={3}".format(
        app_name, api_key, mask_text(secret_key), owner))
    apiKey = ApiKey(app_name=app_name, api_key=api_key,
                    secret_key=secret_key, is_default=0, owner=owner)

    # https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session
    local_object = db.merge(apiKey)
    try:
        db.add(local_object)
        db.commit()
        db.flush()
        return apiKey, None
    except Exception as e:
        return None, str(e)


def delete_api_key(app_name: str, api_key: str, owner: User, db: Session) -> APIKey:
    logging.info("delete_api_key: app_name={0} api_key={1} owner={2}".format(
        app_name, api_key, owner))
    found_apikey = db.query(ApiKey).filter_by(
        app_name=app_name, api_key=api_key).first()
    if found_apikey:
        db.delete(found_apikey)
        db.commit()
        db.flush()


def set_default_api_key(app_name: str, api_key: str, owner: User, db: Session) -> APIKey:
    logging.info("set_default_api_key: app_name={0} api_key={1} owner={2}".format(
        app_name, api_key, owner))
    try:
        # set all is_default to 0
        db.query(ApiKey).filter_by(
            app_name=app_name).update({ApiKey.is_default: 0})

        # set selected is_default to 1
        result = db.query(ApiKey).filter_by(
            app_name=app_name, api_key=api_key).first()
        result.is_default = 1

        # commit
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
