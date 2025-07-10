import json
from faker import Faker
from datetime import datetime
import random
from django.utils.text import slugify

fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# Attribute Data Generation
################################

def generate_attributes():
    data = []
    pk_counter = 1

    for _ in range(15):
        name = fake.unique.word().capitalize()
        slug = slugify(name)
        description = fake.text(max_nb_chars=200)
        is_filterable = random.choice([True, False])

        attribute = {
            "pk": pk_counter,
            "model": "Product.attribute",
            "fields": {
                "name": name,
                "slug": slug,
                "description": description,
                "is_filterable": is_filterable,
                "created_at": now,
                "updated_at": now,
            },
        }
        data.append(attribute)
        pk_counter += 1

    with open("seeders/Fake_data/Attribute.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    generate_attributes()

     


