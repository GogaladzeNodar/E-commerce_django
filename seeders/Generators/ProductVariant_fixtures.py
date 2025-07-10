import json
from faker import Faker
from datetime import datetime
import random
from django.utils.text import slugify


fake = Faker()
now = datetime.utcnow().isoformat() + "Z"


################################
# ProductVariant Data Generation
################################

def generate_product_variants():
    data = []
    pk_counter = 1

    for _ in range(200):
        
        ProductVariant = {
            "model": "Product.ProductVariant",
            "pk": pk_counter,
            "fields": {
                "product": random.randint(1, 70),  # Assuming there are 70 products
                "sku": fake.unique.bothify(text='SKU-###???'),
                "price": round(random.uniform(10.0, 500.0), 2),
                "stock": random.randint(0, 100),
                "image": fake.image_url(width=640, height=480),
                "is_active": random.choice([True, False]),
                "created_at": now,
                "updated_at": now,
            },
        }

        data.append(ProductVariant)
        pk_counter += 1

    with open("seeders/Fake_data/ProductVariant.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    generate_product_variants()
