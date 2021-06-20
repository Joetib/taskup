from backend import ma

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init Schema

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)