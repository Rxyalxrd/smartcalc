from typing import Any
from pydantic import BaseModel, Field, PositiveFloat, RootModel

from app.utils.const.load_yaml_const import open_yaml
from app.utils.const.enum_const import TempMode


descriptions = open_yaml("schemas_const.yaml")
json_schema_extra = open_yaml("json_schema_extra.yaml")


class ComputeConstruction(BaseModel):
    """Базовая схема для расчетов."""

    temp_mode: TempMode = Field(..., description=descriptions["temp_mode"])
    ptm: PositiveFloat = Field(..., description=descriptions["ptm"])
    temp_critical: float = Field(
        ..., description=descriptions["temp_critical"]
    )
    temp_start: float = Field(..., description=descriptions["temp_start"])
    coeff_heat_transfer: PositiveFloat = Field(
        ..., description=descriptions["coeff_heat_transfer"]
    )
    medium_blackness: PositiveFloat = Field(
        ..., gt=0.0, le=1.0, description=descriptions["medium_blackness"]
    )
    density: PositiveFloat = Field(..., description=descriptions["density"])
    metal_blackness: PositiveFloat = Field(
        ..., gt=0.0, le=1.0, description=descriptions["metal_blackness"]
    )
    heat_capacity: PositiveFloat = Field(
        ..., description=descriptions["heat_capacity"]
    )
    coeff_dif_heat_capacity: PositiveFloat = Field(
        ..., description=descriptions["coeff_dif_heat_capacity"]
    )


class ComputeConstructionCreate(ComputeConstruction):
    """
    Схема создания.

    Создание теплотехнического расчета одного элемента конструкции.
    """

    class Config:
        extra = 'forbid'
        json_schema_extra: str | dict[str, Any] = json_schema_extra.get(
            "ComputeConstructionCreate", {}
        )


class ComputeConstructionsCreate(ComputeConstruction):
    """
    Схема создания.

    Создание теплотехнического расчета нескольких элемента конструкции.
    """

    class Config:
        extra = 'forbid'
        json_schema_extra: str | dict[str, Any] = json_schema_extra.get(
            "ComputeConstructionsCreate", {}
        )


class ComputeConstructionRead(
    RootModel[dict[str, list[ComputeConstruction] | ComputeConstruction]]
):
    """
    Схема получения.

    Получение теплотехнического расчета одного
    или нескольких элемента конструкции.
    """

    class Config:
        json_schema_extra: str | dict[str, Any] = json_schema_extra.get(
            "ComputeConstructionRead", {}
        )
