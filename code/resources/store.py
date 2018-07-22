from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {'message': 'your store is not available'}, 404

        return store.json()

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'message': "Your store '{}' is already exist".format(name)}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except Exception as e:
            return {'message': 'An error occured during insertion process : {}'.format(str(e))}

        return {'message': "Your store {} has been added successfully".format(name)}

    def delete(self, name):

        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'your store is not available'}, 404

        try:
            store.delete_from_db()
        except Exception as s:
            return {'message': 'An error occured during deletion process : {}'.format(str(e))}

        return {'message': 'delete store successfully!'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
