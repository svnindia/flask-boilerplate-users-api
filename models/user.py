from database import Database
from bson import ObjectId


class UserModel(object):
    def __init__(self, data, _id: str = None):
        for key in data.keys():
            val = None
            if data[key] is not None:
                val = data[key]
            setattr(self, key, val)

        self._id = str(_id) or None
        self.activated = 0

    @staticmethod
    def find_by_email(email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return data
        return False

    @staticmethod
    def find_by_username(username):
        data = Database.find_one("users", {"username": username})
        if data is not None:
            return data
        return False

    @staticmethod
    def login_valid(email, password):
        user = UserModel.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @staticmethod
    def logout():
        pass

    def json(self):
        # 'password', 'username',  'activated'
        keys = ['email', 'firstName', 'lastName', 'mobile']
        data = {'activated': 1, }
        for key in keys:
            data[key] = getattr(self, key)
        return data

    def save_to_mongo(self):
        if self._id is not None:
            print('save_to_mongo', self.json())
            res = Database.update("users", self._id, self.json())
            print('??????', res)

    def register(self):
        self._id = ObjectId()
        keys = ['email', 'password', 'username', '_id', 'activated']
        data = {}
        for key in keys:
            data[key] = getattr(self, key)
        Database.insert("users", data)
