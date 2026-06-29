from config.settings import settings


def test_app_name_exists():
    assert settings.app_name


def test_port_is_integer():
    assert isinstance(settings.port, int)


def test_log_level_exists():
    assert settings.log_level
