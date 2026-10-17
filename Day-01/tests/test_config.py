
from pathlib import Path

import yaml


def test_example_configuration_is_valid():
    config_path = (
        Path(__file__).resolve().parents[2]
        / "config"
        / "settings.example.yaml"
    )

    config = yaml.safe_load(
        config_path.read_text(encoding="utf-8-sig")
    )

    assert isinstance(config, dict)
    assert "azure" in config
    assert "project" in config
    assert config["project"]["status"] == "NOT_VERIFIED"
    assert config["project"]["live_azure_calls_approved"] is False
    assert config["azure"]["resource_group"]
    assert config["azure"]["location"]
