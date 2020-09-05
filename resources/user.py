import traceback
from passlib.hash import pbkdf2_sha256
from flask_restful import Resource
from flask import request
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    fresh_jwt_required,
)
from schemas.user import UserSchema
# from blacklist import BLACKLIST
# from libs.mailgun import MailGunException

USER_ALREADY_EXISTS = "A user with that username already exists."
EMAIL_ALREADY_EXISTS = "A user with that email already exists."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
NOT_CONFIRMED_ERROR = (
    "You have not confirmed registration, please check your email <{}>."
)
FAILED_TO_SAVE = "Internal server error. Failed to save user."
FAILED_TO_CREATE = "Internal server error. Failed to create user."
SUCCESS_REGISTER_MESSAGE = "Account created successfully, an email with an activation link has been sent to your email address, please check."

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_json['password'] = pbkdf2_sha256.hash(user_json['password'])
        user = user_schema.load(user_json)
        user = UserModel(user)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.email):
            return {"message": EMAIL_ALREADY_EXISTS}, 400

        try:
            user.register()
            # user.send_confirmation_email()
            return {"message": SUCCESS_REGISTER_MESSAGE}, 201
        except:  # failed to save user to db
            traceback.print_exc()
            return {"message": FAILED_TO_CREATE}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        user = UserModel.find_by_username(user_data['username'])

        if user and pbkdf2_sha256.verify(user_json['password'], user['password']):
            if user['activated']:
                access_token = create_access_token(identity=user['username'], fresh=True)
                refresh_token = create_refresh_token(user['username'])
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
            return {"message": NOT_CONFIRMED_ERROR.format(user['email'])}, 400

        return {"message": INVALID_CREDENTIALS}, 401


class UserDetail(Resource):
    @classmethod
    @fresh_jwt_required
    def get(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        me = UserModel.find_by_username(user_id)
        user = UserModel(me, me['_id']).json()
        return user

    @classmethod
    @fresh_jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_username(user_id)
        user_json = request.get_json()
        user_json['password'] = pbkdf2_sha256.hash(user_json['password'])
        body = dict(user_json)
        me = dict(user)
        me.update(body)
        user = UserModel(me, me['_id'])
        try:
            user.save_to_mongo()
            return user.json(), 200
        except:  # failed to save user to db
            traceback.print_exc()
            return {"message": FAILED_TO_SAVE}, 500


