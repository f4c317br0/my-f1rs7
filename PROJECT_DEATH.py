from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto


class IStorageUnit(ABC):
    """Абстрактное место, куда можно положить посылку"""

    @abstractmethod
    def store_item(self, item: 'Parcel') -> bool:
        pass

    @abstractmethod
    def retrieve_item(self, item_id: str) -> Optional['Parcel']:
        pass

    @abstractmethod
    def get_items(self) -> List['Parcel']:
        pass

    @abstractmethod
    def get_capacity(self) -> float:
        pass

    @abstractmethod
    def get_current_load(self) -> float:
        pass

    @abstractmethod
    def get_name_accusative(self) -> str:
        """Название в винительном падеже (на что?): 'на полку 1'"""
        pass

    @abstractmethod
    def get_name_genitive(self) -> str:
        """Название в родительном падеже (с чего?): 'с полки 1'"""
        pass


class IIdentifiable(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass


class Human(IIdentifiable):
    def __init__(self, name: str, passport_id: str):
        self.name = name
        self._passport_id = passport_id

    @property
    def id(self) -> str:
        return self._passport_id

    def speak(self, phrase: str):
        print(f"{self.name} говорит: {phrase}")


class Employee(Human):
    def __init__(self, name: str, passport_id: str, stress_level: int = 0):
        super().__init__(name, passport_id)
        self.stress_level = stress_level


class ParcelStatus(Enum):
    CREATED = auto()
    IN_TRANSIT = auto()
    ARRIVED = auto()
    ISSUED = auto()
    LOST = auto()
    RETURNED = auto()


@dataclass
class Dimensions:
    length: float
    width: float
    height: float

    def volume(self) -> float:
        return self.length * self.width * self.height


@dataclass(order=True)
class Parcel:
    tracking_number: str
    weight_kg: float
    dims: Dimensions
    cost: float
    status: ParcelStatus = field(default=ParcelStatus.CREATED)
    history: list = field(default_factory=list)

    def change_status(self, new_status: ParcelStatus, comment: str = ""):
        self.status = new_status
        self.history.append(f"Статус изменён на {new_status.name}. {comment}")

    def __post_init__(self):
        if self.weight_kg > 30:
            print(f"⚠️ ВНИМАНИЕ: Посылка {self.tracking_number} тяжёлая!")


class FrozenParcel(Parcel):
    def __post_init__(self):
        super().__post_init__()
        self.max_temp_c = -5.0
        print(f"❄️ Внимание! {self.tracking_number} (требует холодильника)")


class FragileParcel(Parcel):
    def __post_init__(self):
        super().__post_init__()
        self.fragil = True
        print(f"⚠️ Хрупкая посылка {self.tracking_number}! Обращаться осторожно.")


@dataclass
class Shelf(IStorageUnit):
    """Обычная полка"""
    max_weight: float
    items: Dict[str, Parcel] = field(default_factory=dict)
    _index: int = 0  # Порядковый номер для имени

    def set_index(self, index: int):
        self._index = index

    def store_item(self, item: Parcel) -> bool:
        if self.get_current_load() + item.weight_kg > self.max_weight:
            return False
        self.items[item.tracking_number] = item
        print(
            f"✅ Посылка {item.tracking_number} положена на полку (нагрузка: {self.get_current_load()}/"
            f"{self.max_weight} кг).")
        return True

    def retrieve_item(self, item_id: str) -> Optional[Parcel]:
        if item_id in self.items:
            item = self.items.pop(item_id)
            print(f"📤 Посылка {item_id} снята с полки.")
            return item
        return None

    def get_items(self) -> List[Parcel]:
        return list(self.items.values())

    def get_capacity(self) -> float:
        return self.max_weight

    def get_current_load(self) -> float:
        return sum(p.weight_kg for p in self.items.values())

    def get_name_accusative(self) -> str:
        return f"полку {self._index}"

    def get_name_genitive(self) -> str:
        return f"полки {self._index}"


class Fridge(Shelf):
    """Холодильник для замороженных посылок"""

    def store_item(self, item: Parcel) -> bool:
        if not isinstance(item, FrozenParcel):
            return False
        return super().store_item(item)

    def get_name_accusative(self) -> str:
        return f"холодильник {self._index}"

    def get_name_genitive(self) -> str:
        return f"холодильника {self._index}"


@dataclass
class FloorCorner(IStorageUnit):
    """Угол для тяжелых посылок"""
    max_items: int
    min_weight: float = 30.0
    items: Dict[str, Parcel] = field(default_factory=dict)
    _index: int = 0

    def set_index(self, index: int):
        self._index = index

    def store_item(self, item: Parcel) -> bool:
        if item.weight_kg < self.min_weight:
            print(f'🚫 Посылка {item.tracking_number} слишком лёгкая для угла!')
            return False
        if len(self.items) >= self.max_items:
            print(f'В углу нет места для {item.tracking_number}!')
            return False
        self.items[item.tracking_number] = item
        print(f'📦 Посылка {item.tracking_number} поставлена в угол (место {len(self.items)}/{self.max_items})')
        return True

    def retrieve_item(self, item_id: str) -> Optional[Parcel]:
        if item_id in self.items:
            item = self.items.pop(item_id)
            print(f'📤 Посылка {item_id} забрана из угла')
            return item
        return None

    def get_items(self) -> List[Parcel]:
        return list(self.items.values())

    def get_capacity(self) -> float:
        return float(self.max_items)

    def get_current_load(self) -> float:
        return float(len(self.items))

    def get_name_accusative(self) -> str:
        return f"угол {self._index}"

    def get_name_genitive(self) -> str:
        return f"угла {self._index}"


class ActionLogger:
    def __init__(self):
        self.logs: List[Tuple[str, str, str, str]] = []

    def log(self, time: str, actor: str, action: str, details: str):
        self.logs.append((time, actor, action, details))
        print(f"[{time}] {actor}: {action} {details}")

    def show(self):
        print("\n=== ЖУРНАЛ СОБЫТИЙ ===")
        for time, actor, action, details in self.logs:
            print(f"[{time}] {actor}: {action} ({details})")


class PickupPoint:
    def __init__(self, address: str, manager: Employee):
        self.address = address
        self.manager = manager
        self.logger = ActionLogger()
        self.storage_units: List[IStorageUnit] = []
        self._shelf_counter = 0

        self.logger.log("00:00:00", manager.name, "открыл ПВЗ", f"по адресу {address}")

    def add_shelf(self, shelf: IStorageUnit, time: str):
        self._shelf_counter += 1
        shelf.set_index(self._shelf_counter)
        self.storage_units.append(shelf)

        # Для сообщения "добавил полку" используем общую форму или винительный, но в примере просто "добавил полку вместимость..."
        # В примере вывода: [10:00:00] Галина Ивановна: добавил полку (вместимость 20.0 кг)
        # Детали: "вместимость ... кг". Само действие "добавил полку" хардкодится или берется от типа?
        # В примере текста лога: "добавил полку вместимость 20.0 кг".
        # Значит action="добавил полку", details="вместимость ...".

        details = f"вместимость {shelf.get_capacity()} кг"
        self.logger.log(time, self.manager.name, "добавил полку", details)

    def receive_parcel(self, parcel: Parcel, courier: Human, time: str):
        self.logger.log(time, courier.name, "принял посылку", parcel.tracking_number)

        placed = False

        for unit in self.storage_units:
            # Проверка типа для замороженных
            if isinstance(parcel, FrozenParcel) and not isinstance(unit, Fridge):
                continue

            # Попытка размещения
            if unit.store_item(parcel):
                unit_name = unit.get_name_accusative()
                self.logger.log(time, self.manager.name, "разместил посылку",
                                f"{parcel.tracking_number} на {unit_name}")
                placed = True
                break
            else:
                # Логирование отказа только если тип подходит, но не влезло
                if isinstance(parcel, FrozenParcel) and isinstance(unit, Fridge):
                    self.logger.log(time, self.manager.name, "не подошла полка",
                                    f"{parcel.tracking_number} — полка отказала")

        if not placed:
            self.logger.log(time, self.manager.name, "НЕ удалось разместить посылку",
                            f"{parcel.tracking_number} — нет подходящего места")

    def serve_client(self, client: Human, tracking_number: str, time: str):
        self.logger.log(time, client.name, "запрос на выдачу", tracking_number)

        found_unit = None
        item = None

        for unit in self.storage_units:
            item = unit.retrieve_item(tracking_number)
            if item:
                found_unit = unit
                break

        if item:
            unit_name = found_unit.get_name_genitive()
            self.logger.log(time, self.manager.name, "снял посылку", f"{tracking_number} с {unit_name}")
            self.logger.log(time, self.manager.name, "выдал посылку", f"{tracking_number} клиенту {client.name}")
            item.change_status(ParcelStatus.ISSUED)
        else:
            self.logger.log(time, self.manager.name, "посылка не найдена", tracking_number)


if __name__ == '__main__':
    dim = Dimensions(10, 10, 10)

    galya = Employee("Галина Ивановна", "PASS-999", stress_level=50)
    courier = Human("Курьер Вася", "PASS-777")
    client1 = Human("Анна Петровна", "PASS-111")

    pvz = PickupPoint("ул. Ленина, д. 1", galya)

    shelf1 = Shelf(20.0)
    pvz.add_shelf(shelf1, "10:00:00")

    parcel1 = Parcel("TRACK-001", 5.0, dim, 500.00)
    parcel2 = Parcel("TRACK-002", 15.0, dim, 1500.00)

    pvz.receive_parcel(parcel1, courier, "10:15:00")
    pvz.receive_parcel(parcel2, courier, "10:16:00")

    pvz.serve_client(client1, "TRACK-001", "11:00:00")

    pvz.logger.show()
