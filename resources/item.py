from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    # reqparse.RequestParser() dapat digunakan untuk memastikan data yang dikirimkan sudah sesuai, melalui validasi
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id.')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        # force=True; maksudnya agar request yang datang tidak mesti ada request header content-type : application/json
        # data = request.get_json(force=True)

        # data = request.get_json()
        data = Item.parser.parse_args()
        # item = {'name': name, 'price': data['price']}
        item = ItemModel(name, **data)
        # items.append(item)

        try:
            # ItemModel.insert(item)
            # item.insert()
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'DELETE FROM items WHERE name=?'
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # update_item = ItemModel(name, data['price'])

        if item is None:
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
            # try:
            #     # ItemModel.insert(update_item)
            #     update_item.insert()
            # except:
            #     return {'message': 'An error occurred inserting the item.'}, 500

            item = ItemModel(name, **data)
        else:
            # item.update(data)
            # try:
            #     # ItemModel.update(update_item)
            #     update_item.update()
            # except:
            #     return {'message': 'An error occurred updating the item.'}, 500

            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        #
        # connection.close()
        #
        # return {'items': items}
        return {'items': [x.json() for x in ItemModel.query.all()]}

