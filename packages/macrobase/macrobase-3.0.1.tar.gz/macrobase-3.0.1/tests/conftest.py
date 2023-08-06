import pytest

from macrobase.app import Application, AppConfig
from tests.sample_app import SampleApplication


@pytest.fixture(scope='class')
def app_config() -> AppConfig:
    return AppConfig(file='configs/app_config.yaml')


@pytest.fixture(scope='class')
def application(app_config: AppConfig) -> Application:
    return Application(config=app_config, name='Application')


@pytest.fixture(scope='class')
def sample_app(application: Application) -> SampleApplication:
    return SampleApplication()
