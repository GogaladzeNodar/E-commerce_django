import json
from faker import Faker
from datetime import datetime
from django.utils.text import slugify


fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# Category Data Generation
################################


def assign_mptt_fields(nodes):
    tree_id = 1

    # აქ ვქმნით lookup-ს: parent_pk -> list of children
    children_map = {}
    for node in nodes:
        parent = node['parent']
        children_map.setdefault(parent, []).append(node)

    counter = 1

    def recurse(node, mptt_level):
        nonlocal counter
        node['tree_id'] = tree_id
        node['mptt_level'] = mptt_level
        node['lft'] = counter
        counter += 1
        # შვილები
        for child in children_map.get(node['pk'], []):
            recurse(child, mptt_level + 1)
        node['rght'] = counter
        counter += 1

    # დავიწყოთ root-ებიდან (parent = None)
    for root in children_map.get(None, []):
        recurse(root, 0)

def generate_categories_with_mptt():
    data = []
    pk_counter = 1
    parent_ids = []

    # დაგენერირე nodes წინასწარ როგორც "არაპოლიმორფული" dict-ები MPTT-ს გარეშე
    nodes = []

    # Root categories
    for _ in range(3):
        name = fake.unique.word().capitalize()
        node = {
            "model": "Product.category",
            "pk": pk_counter,
            "fields": {
                "name": name,
                "slug": slugify(name),
                "is_active": True,
                "parent": None,
                "created_at": now,
                "updated_at": now,
                # MPTT ველები აქ ჯერ არ არის
            }
        }
        nodes.append({"pk": pk_counter, "parent": None, "node": node})
        pk_counter += 1

    # Children
    for root in [n for n in nodes if n['parent'] is None]:
        for _ in range(2):
            name = fake.unique.word().capitalize()
            node = {
                "model": "Product.category",
                "pk": pk_counter,
                "fields": {
                    "name": name,
                    "slug": slugify(name),
                    "is_active": True,
                    "parent": root['pk'],
                    "created_at": now,
                    "updated_at": now,
                }
            }
            nodes.append({"pk": pk_counter, "parent": root['pk'], "node": node})
            pk_counter += 1

    # MPTT ველების გამოთვლა
    # ვთარგმნით simplified nodes სიუჟეტად (pk, parent)
    simple_nodes = [{"pk": n["pk"], "parent": n["parent"]} for n in nodes]
    assign_mptt_fields(simple_nodes)

    # ახლა each node-ს fields-ში დავამატოთ MPTT ველები
    for simple_node in simple_nodes:
        pk = simple_node['pk']
        # მოძებნე node
        original = next(n['node'] for n in nodes if n['pk'] == pk)
        original['fields']['lft'] = simple_node['lft']
        original['fields']['rght'] = simple_node['rght']
        original['fields']['tree_id'] = simple_node['tree_id']
        original['fields']['mptt_level'] = simple_node['mptt_level']

    # საბოლოოდ, გვჭირდება მხოლოდ node dict-ები, არა ზედმეტი მონაცემები
    data = [n['node'] for n in nodes]

    with open("seeders/Fake_data/categories_with_mptt.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated {len(data)} categories with MPTT fields in categories_with_mptt.json")


if __name__ == "__main__":
    generate_categories_with_mptt()
