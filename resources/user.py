import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )

    def post(self):

        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            return {"user": "user is already exist"}

        try:
            user = UserModel(data['username'], data['password'])
            user.insert()
        except Exception as e:
            return {'message': str(e)}

        return {"message": "Insert data successfully !"}, 200


class UserList(Resource):

    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
