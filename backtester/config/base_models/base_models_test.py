import os
from typing import Optional
from uuid import UUID, uuid4

import pytest
from pydantic_settings import BaseSettings

from config.base_models.base_models import CustomConfigsSource, BaseModel, SubBaseModel

@pytest.fixture(autouse=True)
def reset_env():
    os.environ.pop("DUMMY_PROPERTY", None)
    os.environ.pop("DUMMY_SUB_MODEL__DUUMY_SUB_PROPERTY", None)
    os.environ.pop("DUMMY_SUB_MODEL__DUUMY_SUB_PROPERTY_WITH_SAME_NAME", None)
    os.environ.pop("DUUMY_SUB_PROPERTY_WITH_SAME_NAME", None)

class DummySubModel(SubBaseModel):
    dummy_property_with_same_name: Optional[str] = None
    dummy_sub_property: Optional[str] = None

class DummyModel(BaseModel):
    id: UUID
    dummy_property_with_same_name: Optional[str] = None
    dummy_property: Optional[str] = None
    dummy_sub_model: Optional[DummySubModel] = None


def test_sub_config_model_raises_error_when_setting_attribute():
    new_model = DummySubModel(dummy_sub_property="value")

    with pytest.raises(Exception):
        new_model.dummy_sub_property = "new_value"