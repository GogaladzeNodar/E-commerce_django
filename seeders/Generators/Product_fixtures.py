import random
from faker import Faker
import json
from datetime import datetime
from django.utils.text import slugify



fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# Product Data Generation
################################

def generate_products():
    data = []
    pk_counter = 1

    for _ in range(70):
        name = fake.unique.word().capitalize()
        slug = slugify(name)

        product = {
            "model": "Product.Product",
            "pk": pk_counter,
            "fields": {
                "name": name,
                "slug": slug,
                "description": fake.text(max_nb_chars=200),
                "categories": random.sample(range(1, 10), k=random.randint(1, 3)),  
                "product_type": random.choice(range(1, 51)), 
                "tags": random.sample(range(1, 21), k=random.randint(0, 5)),
                "image": fake.image_url(width=640, height=480),
                "is_active": random.choices([True, False], weights=[0.7, 0.3])[0],
                "created_at": now,
                "updated_at": now,
            },
        }
        data.append(product)
        pk_counter += 1

    with open("seeders/Fake_data/Product.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    generate_products()
