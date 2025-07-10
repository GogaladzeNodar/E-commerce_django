import json
from faker import Faker
from datetime import datetime
import random
from django.utils.text import slugify



fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# Attribute Value Data Generation
################################

def generate_attribute_values():
    data = []
    pk_counter = 1

    for _ in range(50):
        value = fake.unique.word().capitalize()
        slug = slugify(value)
        attribute_id = random.randint(1, 15)  # Assuming there are 15 attributes

        attribute_value = {
            "model": "Product.AttributeValue",
            "pk": pk_counter,
            "fields": {
                "value": value,
                "slug": slug,
                "attribute": attribute_id,
                "created_at": now,
                "updated_at": now,
            },
        }
        data.append(attribute_value)
        pk_counter += 1

    with open("seeders/Fake_data/AttributeValue.json", "w") as f:
        json.dump(data, f, indent=2)
    

if __name__ == "__main__":
    generate_attribute_values()




