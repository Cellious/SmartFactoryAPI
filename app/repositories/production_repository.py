from app.database.fake_db import production_records


def get_all_production():
    return production_records


def get_production_by_id(production_id: int):
    for record in production_records:
        if record["id"] == production_id:
            return record

    return None


def create_production(production_data: dict):
    new_id = max(
        record["id"]
        for record in production_records
    ) + 1

    record = {
        "id": new_id,
        **production_data,
    }

    production_records.append(record)

    return record


def update_production(
    production_id: int,
    production_data: dict,
):
    record = get_production_by_id(production_id)

    if record is None:
        return None

    for key, value in production_data.items():
        if value is not None:
            record[key] = value

    return record


def delete_production(production_id: int):
    record = get_production_by_id(production_id)

    if record is None:
        return False

    production_records.remove(record)

    return True
