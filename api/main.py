import io
import random
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
    print("\n\n#######################")
    print("#                     #")
    print("# Deleting categories #")
    print("#                     #")
    print("#######################\n")

    categories = prestashop.get('categories')
    if categories:
        category_ids = []
        for category in categories['categories']['category']:
            category_id = int(category['attrs']['id'])
            if category_id not in [1, 2]:
                category_ids.append(category_id)
                
        if category_ids:
            try:
                prestashop.delete("categories", resource_ids=category_ids)
                print(f"Deleted {len(category_ids)} categories")
            except:
                print("[ERROR] Error while deleting categories")
                
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
        change_quantity(product_id)
        load_product_images(product_id, product["images"])

def load_product(product):
    try:
        product_categories = []
        for category_name in product["categories"]:
            category = prestashop.get("categories", options={
                "filter[name]": category_name
            })
            category_id = category["categories"]["category"]["attrs"]["id"]
            product_categories.append(category_id)

        product_schema["product"]["link_rewrite"]["language"]["value"] = re.sub(
            r"[^a-zA-Z0-9]+", "-", product["name"]).lower()
        product_schema['product']['name']['language']['value'] = product["name"]
        product_schema["product"]["meta_title"]["language"]["value"] = product["name"]
        product_schema["product"]["id_shop_default"] = 1
        product_schema["product"]["reference"] = str(product["sku"])
        product_schema["product"]["id_tax_rules_group"] = 1
        product_schema['product']['price'] = round(float(product["price"].replace(',', ''))/1.23, 0)
        product_schema["product"]["weight"] = round((random.randint(100, 5000)/1000), 3)
        product_schema['product']['description']['language']['value'] = product["description"]
        product_schema['product']['description_short']['language']['value'] = product["short_description"]
        product_schema["product"]["active"] = 1
        product_schema["product"]["state"] = 1
        product_schema["product"]["available_for_order"] = 1
        product_schema["product"]["minimal_quantity"] = 1
        product_schema["product"]["show_price"] = 1
        product_schema['product']['id_category_default'] = product_categories[0]
        product_schema["product"]["associations"]["categories"] = {
            "category": [{"id": category_id} for category_id in product_categories]
        }
        product_schema["product"]["associations"]["categories"]["category"].append({"id": 2})

        response = prestashop.add('products', product_schema)
        product_id = response['prestashop']['product']['id']
        print(f"Added product {product_id}: {product['name']}")
        return product_id
    except Exception as e:
        print(f"[ERROR] Error while adding product {product['name']}: {e}")
        
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
    print("\n\n#######################")
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
        if product_ids:
            try: 
                prestashop.delete("products", resource_ids=product_ids)
                print(f"Deleted {len(product_ids)} products")
            except: 
                print("[ERROR] Error while deleting products")
                

    features = prestashop.get("product_features")["product_features"]
    if features:
        features_data = prestashop.get("product_features")[
            "product_features"]["product_feature"]

        if isinstance(features_data, dict):
            features_data = [features_data]

        feature_ids = [int(feature["attrs"]["id"]) for feature in features_data]
        if feature_ids:
            try:
                prestashop.delete("product_features", resource_ids=feature_ids)
                print(f"Deleted {len(feature_ids)} features")
            except:
                print("[ERROR] Error while deleting features")
                

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
