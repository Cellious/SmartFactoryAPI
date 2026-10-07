from app.database.fake_db import machines, production_records


def calculate_machine_performance():
    reports = []

    for machine in machines:
        machine_id = machine["id"]

        machine_records = [
            record
            for record in production_records
            if record["machine_id"] == machine_id
        ]

        total_production = sum(
            record["quantity"]
            for record in machine_records
        )

        total_scrap = sum(
            record["scrap_quantity"]
            for record in machine_records
        )

        if total_production == 0:
            scrap_rate = 0
        else:
            scrap_rate = (
                total_scrap / total_production
            ) * 100

        reports.append(
            {
                "machine": machine["code"],
                "machine_name": machine["name"],
                "total_production": total_production,
                "total_scrap": total_scrap,
                "scrap_rate": round(scrap_rate, 2),
            }
        )

    return reports
