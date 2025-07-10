from faker import Faker
import json
from datetime import datetime
from django.utils.text import slugify
import random


fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# ProductType Data Generation
################################

def generate_product_types():
    data = []
    pk_counter = 1

    for _ in range(50):
        name = fake.unique.word().capitalize()
        slug = slugify(name)

        product_type = {
            "model": "Product.ProductType",
            "pk": pk_counter,
            "fields": {
                "name": name,
                "slug": slug,
                "is_active": random.choices([True, False], weights=[0.7, 0.3])[0],
                "created_at": now,
                "updated_at": now,
            },
        }
        data.append(product_type)
        pk_counter += 1
    



    with open("seeders/Fake_data/ProductType.json", "w") as f:
        json.dump(data, f, indent=2)



if __name__ == "__main__":
    generate_product_types()
