from app.database.fake_db import products


def get_all_products():
    return products


def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return None


def create_product(product_data: dict):
    new_id = max(product["id"] for product in products) + 1

    product = {
        "id": new_id,
        **product_data,
    }

    products.append(product)

    return product


def update_product(product_id: int, product_data: dict):
    product = get_product_by_id(product_id)

    if product is None:
        return None

    for key, value in product_data.items():
        if value is not None:
            product[key] = value

    return product


def delete_product(product_id: int):
    product = get_product_by_id(product_id)

    if product is None:
        return False

    products.remove(product)

    return True


def get_low_stock_products():
    return [
        product
        for product in products
        if product["stock"] <= product["min_stock"]
    ]