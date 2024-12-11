from enum import Enum


class TempMode(str, Enum):
    MODE_STANDART = "Стандартный"
    MODE_HYDROCARBON = "Углеводородный"
    MODE_EXTERNAL = "Наружный"
    MODE_SMOLDERING = "Тлеющий"
