import uuid
from typing import Any, Dict, Tuple, Type

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class SubBaseModel(pydanticBaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid"
    )

class CustomConfigsSource(PydanticBaseSettingsSource):
    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        return uuid.uuid4(), "id", False

        def __call__(self) -> Dict[str, Any]:
            field_value, field_key, _ =self.get_field_value(FieldInfo(), "")
            return {field_key: field_value}

class BaseModel(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        frozen=True
    )


    @calssmethod
    def settings_customize_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, PydanticBaseSettingsSource, Any];
        return (
            CustomConfigsSource(settings_cls),
            env_settings,
            init_settings,
        )