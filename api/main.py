import io
import re
import json
import os
from random import randint
from prestapyt import PrestaShopWebServiceDict

DEFAULT_LINK = "http://localhost:8080/api/"
API_KEY = "JKCTYYE6FNEQRR3R3NFHM63VZ8FBPS72"

def load_categories():
    delete_all_categories()

    with open("../results/categories.json") as file:
        categories = json.load(file)

    print("\n\n#######################")
    print("#                     #")
    print("#  Adding categories  #")
    print("#                     #")
    print("#######################\n")
    index = 2
    for category, subcategories in categories.items():
        parent_category_id = load_category(category, index)
        print(f"Added category {category}")
        for subcategory, subsubcategories in subcategories.items():
            subcategory_id = load_category(subcategory, parent_category_id)
            print(f"Added category {subcategory}")
            for subsubcategory in subsubcategories:
                load_category(subsubcategory, subcategory_id)
                print(f"Added category {subsubcategory}")

def load_category(name: str, parent_id: int = None):
    category = prestashop.get('categories', options={
        'filter[name]': name
    })

    if not category["categories"]:
        category_schema['category']['name']['language']['value'] = name
        category_schema['category']['id_parent'] = parent_id or '2'
        category_schema["category"]["active"] = 1
        response = prestashop.add('categories', category_schema)
        category_id = response['prestashop']['category']['id']
    else:
        category_id = category["categories"]["category"]["attrs"]["id"]

    return category_id

def delete_all_categories():
    print("\n#######################")
    print("#                     #")
    print("# Deleting categories #")
    print("#                     #")
    print("#######################\n")
    categories = prestashop.get('categories')
    for category in categories['categories']['category']:
        category_id = int(category['attrs']['id'])
        if category_id not in [1, 2]:
            try:
                prestashop.delete("categories", resource_ids=category_id)
                print(f"Deleted category {category_id}")
            except:
                print("[ERROR] Error while deleting category")
                
def load_products():
    delete_all_products()
    with open("../results/products.json") as file:
        products = json.load(file)

    print("\n\n#######################")
    print("#                     #")
    print("#  Adding products    #")
    print("#                     #")
    print("#######################\n")
    for product in products:
        product_id = load_product(product)
        print("Product_ID: ", product_id)
        change_quantity(product_id)
        # load_product_images(product_id, product["images"])

def load_product(product):
    try:
        default_category = prestashop.get("categories", options={
            "filter[name]": product["categories"][0]
        })
        default_category_id = default_category["categories"]["category"]["attrs"]["id"]
        product_schema["product"]["link_rewrite"]["language"]["value"] = re.sub(
            r"[^a-zA-Z0-9]+", "-", product["name"]).lower()
        product_schema['product']['id_category_default'] = default_category_id
        product_schema['product']['name']['language']['value'] = product["name"]
        product_schema["product"]["meta_title"]["language"]["value"] = product["name"]
        product_schema["product"]["id_shop_default"] = 1
        product_schema["product"]["reference"] = int(product["sku"])
        product_schema["product"]["id_tax_rules_group"] = 1
        product_schema['product']['price'] = round(float(product["price"])/1.23, 2)
        product_schema['product']['description']['language']['value'] = product["description"]
        product_schema['product']['description_short']['language']['value'] = product["short_description"]
        product_schema["product"]["active"] = 1
        product_schema["product"]["state"] = 1
        product_schema["product"]["available_for_order"] = 1
        product_schema["product"]["minimal_quantity"] = 1
        product_schema["product"]["show_price"] = 1
        response = prestashop.add('products', product_schema)
        print(f"Added product {product['name']}")
        return response['prestashop']['product']['id']
    except Exception as e:
        print(e)
        
def change_quantity(product_id: int) -> None:
    schema_id = prestashop.search("stock_availables", options={
        "filter[id_product]": product_id
    })[0]
    stock_available_schema = prestashop.get(
        "stock_availables", resource_id=schema_id)
    stock_available_schema["stock_available"]["quantity"] = randint(0, 10)
    stock_available_schema["stock_available"]["depends_on_stock"] = 0
    prestashop.edit("stock_availables", stock_available_schema)

def load_product_images(product_id: int, images_names: [str]):
    for image_name in images_names:
        image_path = f"../results/images/{image_name}"
        if os.path.exists(image_path):
            file = io.open(image_path, 'rb')
            image_data = file.read()
            file.close()
            prestashop.add(f"images/products/{product_id}", files=[('image', image_name, image_data)])
            print(f"Added image {image_name} to product {product_id}")

def delete_all_products():
    print("\n#######################")
    print("#                     #")
    print("# Deleting products   #")
    print("#                     #")
    print("#######################\n")
    products = prestashop.get("products")["products"]
    if products:
        products_data = products["product"]

        if isinstance(products_data, dict):
            products_data = [products_data]

        product_ids = [int(product["attrs"]["id"]) for product in products_data]
        for id in product_ids:
            try: 
                prestashop.delete("products", resource_id=id)
                print(f"Deleted product {id}")
            except: 
                print("[ERROR] Error while deleting product")
                

    features = prestashop.get("product_features")["product_features"]
    if features:
        features_data = prestashop.get("product_features")[
            "product_features"]["product_feature"]

        if isinstance(features_data, dict):
            features_data = [features_data]

        feature_ids = [int(feature["attrs"]["id"]) for feature in features_data]
        for id in feature_ids:
            try:
                prestashop.delete("product_features", resource_id=id)
                print(f"Deleted feature {id}")
            except:
                print("[ERROR] Error while deleting feature")
                

if __name__ == "__main__":
    prestashop = PrestaShopWebServiceDict(DEFAULT_LINK, API_KEY)

    category_schema = prestashop.get('categories', options={
        'schema': 'blank'
    })

    product_schema = prestashop.get('products', options={
        'schema': 'blank'
    })

    del product_schema["product"]["position_in_category"]
    del product_schema["product"]["associations"]["combinations"]

    image_schema = prestashop.get('images/products', options={
        'schema': 'blank'
    })

    load_categories()
    load_products()
