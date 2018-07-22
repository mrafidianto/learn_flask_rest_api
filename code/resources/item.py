from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left black'
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs store id'
                        )

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'Item not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': "Your item {} is already in the list".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            ItemModel.insert(item)
        except:
            return {'message': 'An error occured during insertion process'}, 500

        return item.json(), 201

    def delete(self, name):

        check_item = ItemModel.find_by_name(name)

        if check_item:
            check_item.delete_from_db()

            return {'message': 'Item {} deleted !'.format(name)}
        else:
            return {'message': "Your item '{}' is not available yet!".format(name)}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        mode = ""

        if item is None:

            item = ItemModel(name, data['price'], data['store_id'])
            mode = "insertion process"
        else:

            item.price = data['price']
            item.store_id = data['store_id']
            mode = "updating process"
        try:
            item.save_to_db()
        except Exception as e:
            return {'message': 'An error occured during ' + mode + " : "+str(e)}

        return item.json()


class ItemList(Resource):

    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
