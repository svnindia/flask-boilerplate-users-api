import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from database import Database
from resources.user import (
    UserRegister,
    UserLogin,
    UserDetail
    # User,
    # TokenRefresh,
    # UserLogout,
    # UserConfirm,
)


app = Flask(__name__)
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.secret_key = os.environ.get(
    "APP_SECRET_KEY"
) or 'mysecret123'  # could do app.config['JWT_SECRET_KEY'] if we prefer

api = Api(app)
jwt = JWTManager(app)


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    pass
    # return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserDetail, "/me")

if __name__ == '__main__':
    Database.initialize()
    app.run()
