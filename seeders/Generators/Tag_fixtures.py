import random
from faker import Faker
import json
from datetime import datetime
from django.utils.text import slugify


fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# Tag Data Generation
################################

def generate_tags():
    data = []
    pk_counter = 1

    for _ in range(20):
        name = fake.unique.word().capitalize()
        slug = slugify(name)

        tag = {
            "model": "Product.Tag",
            "pk": pk_counter,
            "fields": {
                "name": name,
                "slug": slug,
                "is_active": random.choices([True, False], weights=[0.7, 0.3])[0],
                "created_at": now,
                "updated_at": now,
            },
        }
        data.append(tag)
        pk_counter += 1

    with open("seeders/Fake_data/Tag.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    generate_tags()
    
                