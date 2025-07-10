import json
import random
from faker import Faker
from django.utils.text import slugify
from datetime import datetime

fake = Faker()
now = datetime.utcnow().isoformat() + "Z"

################################
# Product Variant Attribute Value Data Generation
################################

def generate_product_variant_attribute_values():
    used_combinations = set()  
    data = []
    pk_counter = 1

    for _ in range(400):
        variant_id = random.randint(1, 200)  # Assuming there are 200 variants
        attribute_id = random.randint(1, 15)  # Assuming there are 15 attributes
        attribute_value_id = random.randint(1, 50)  # Assuming there are 50 attribute values


        key = (variant_id, attribute_id)
        if key in used_combinations:
            continue
        

        used_combinations.add(key)


        product_variant_attribute_value = {
            "model": "Product.ProductVariantAttributeValue",
            "pk": pk_counter,
            "fields": {
                "variant": variant_id,
                "attribute": attribute_id,
                "attribute_value": attribute_value_id,
                "created_at": now,
                "updated_at": now,
            },
        }
        data.append(product_variant_attribute_value)
        pk_counter += 1

    with open("seeders/Fake_data/ProductVariantAttributeValue.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    generate_product_variant_attribute_values()

