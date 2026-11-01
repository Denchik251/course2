"""Рубежный контроль №1: вариант 8 (Жёсткий диск — Компьютер)."""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class HardDrive:
    """Жёсткий диск: первичный ключ, название, объём (ГБ), ID компьютера."""

    id: int
    name: str
    capacity_gb: int
    computer_id: int


@dataclass(frozen=True)
class Computer:
    """Компьютер: первичный ключ и наименование."""

    id: int
    name: str


@dataclass(frozen=True)
class HardDriveComputer:
    """Промежуточный класс для отношения многие-ко-многим."""

    drive_id: int
    computer_id: int


computers = [
    Computer(1, "Архивный компьютер"),
    Computer(2, "Альфа ПК"),
    Computer(3, "Игровой компьютер"),
    Computer(4, "Офисный компьютер"),
]

drives = [
    HardDrive(1, "Альфа", 512, 1),
    HardDrive(2, "Атласов", 1024, 1),
    HardDrive(3, "Барсов", 2048, 2),
    HardDrive(4, "Вектор", 256, 3),
    HardDrive(5, "Астра", 1000, 3),
]

# В рамках many-to-many диск можно связать и с дополнительными компьютерами.
drive_computers = [
    HardDriveComputer(1, 1), HardDriveComputer(1, 2),
    HardDriveComputer(2, 1), HardDriveComputer(2, 4),
    HardDriveComputer(3, 2), HardDriveComputer(3, 3),
    HardDriveComputer(4, 3), HardDriveComputer(4, 4),
    HardDriveComputer(5, 3), HardDriveComputer(5, 1),
]


def build_relations():
    """Соединяет таблицы по ID, не по названиям объектов."""
    computer_by_id = {computer.id: computer for computer in computers}
    drive_by_id = {drive.id: drive for drive in drives}
    one_to_many = [
        (drive.name, drive.capacity_gb, computer_by_id[drive.computer_id].name)
        for drive in drives
    ]
    many_to_many = [
        (drive_by_id[link.drive_id].name,
         drive_by_id[link.drive_id].capacity_gb,
         computer_by_id[link.computer_id].name)
        for link in drive_computers
    ]
    return one_to_many, many_to_many


def grouped_by_computer(relation):
    return {
        computer.name: [drive_name for drive_name, _, name in relation if name == computer.name]
        for computer in computers
    }


def capacity_stat(relation, operation):
    result = []
    for computer in computers:
        sizes = [capacity for _, capacity, name in relation if name == computer.name]
        if not sizes:
            continue
        value = {
            "sum": lambda: sum(sizes),
            "count": lambda: len(sizes),
            "min": lambda: min(sizes),
            "max": lambda: max(sizes),
            "average": lambda: sum(sizes) / len(sizes),
            "rounded_average": lambda: round(sum(sizes) / len(sizes), 2),
        }[operation]()
        result.append((computer.name, value))
    return sorted(result, key=lambda row: (row[1], row[0]))


def run_queries(letter):
    """Возвращает ответы на все три запроса выбранного буквенного варианта."""
    one, many = build_relations()
    starts_a = lambda name: name.lower().startswith("а")
    ends_ov = lambda name: name.lower().endswith("ов")
    has_computer = lambda name: "компьютер" in name.lower()

    if letter == "А":
        return (
            sorted(one, key=lambda row: (row[2], row[0])),
            capacity_stat(one, "sum"),
            {name: drives_list for name, drives_list in grouped_by_computer(many).items()
             if has_computer(name)},
        )
    if letter == "Б":
        return (
            sorted(one, key=lambda row: (row[0], row[2])),
            capacity_stat(one, "count"),
            [(drive, computer) for drive, _, computer in many if ends_ov(drive)],
        )
    if letter == "В":
        return (
            [(drive, computer) for drive, _, computer in one if starts_a(drive)],
            capacity_stat(one, "min"),
            sorted(many, key=lambda row: (row[0], row[2])),
        )
    if letter == "Г":
        return (
            {name: items for name, items in grouped_by_computer(one).items()
             if starts_a(name)},
            capacity_stat(one, "max"),
            sorted(many, key=lambda row: (row[2], row[0])),
        )
    if letter == "Д":
        return (
            [(drive, computer) for drive, _, computer in one if ends_ov(drive)],
            capacity_stat(one, "average"),
            {name: items for name, items in grouped_by_computer(many).items()
             if starts_a(name)},
        )
    if letter == "Е":
        return (
            {name: items for name, items in grouped_by_computer(one).items()
             if has_computer(name)},
            capacity_stat(one, "rounded_average"),
            [(drive, computer) for drive, _, computer in many if starts_a(drive)],
        )
    raise ValueError("Допустимые буквенные варианты: А, Б, В, Г, Д, Е")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", default="А", choices=list("АБВГДЕ"),
                        help="Буква варианта запросов (по умолчанию: А)")
    args = parser.parse_args()
    for index, answer in enumerate(run_queries(args.variant), start=1):
        print(f"Задание {args.variant}{index}")
        print(answer)
        print()


if __name__ == "__main__":
    main()
