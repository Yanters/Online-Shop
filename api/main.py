import json
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
        category_schema = prestashop.get('categories', options={
            'schema': 'blank'
        })

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
            except:
                pass
            finally:
                print(f"Deleted category {category_id}")
            

if __name__ == "__main__":
    prestashop = PrestaShopWebServiceDict(DEFAULT_LINK, API_KEY)
    load_categories()