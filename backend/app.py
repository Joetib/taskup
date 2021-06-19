from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from pathlib import Path



BASE_DIR = Path(__file__).parent
print(BASE_DIR)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# initialize marshmallow
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    describtion = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
    
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init Schema

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    qty = request.json['qty']
    price = request.json['price']

    new_product = Product(name=name, description=description, price=price, qty=qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)
@app.route('/product', methods=["GET"])
def get_all_products():
    all_products= Product.query.all()
    results = products_schema.dump(all_products)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)