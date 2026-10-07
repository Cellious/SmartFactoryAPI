from app.database.fake_db import machines


def get_all_machines():
    return machines


def get_machine_by_id(machine_id: int):
    for machine in machines:
        if machine["id"] == machine_id:
            return machine

    return None


def create_machine(machine_data: dict):
    new_id = max(
        machine["id"]
        for machine in machines
    ) + 1

    machine = {
        "id": new_id,
        **machine_data,
    }

    machines.append(machine)

    return machine


def update_machine(
    machine_id: int,
    machine_data: dict,
):
    machine = get_machine_by_id(machine_id)

    if machine is None:
        return None

    for key, value in machine_data.items():
        if value is not None:
            machine[key] = value

    return machine


def delete_machine(machine_id: int):
    machine = get_machine_by_id(machine_id)

    if machine is None:
        return False

    machines.remove(machine)

    return True
