"""Tests for the energieleser sensor platform."""

from unittest.mock import AsyncMock

import pytest
from syrupy.assertion import SnapshotAssertion

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


async def _setup_integration(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
) -> None:
    """Set up the energieleser integration."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    ("device_fixture", "config_entry_fixture"),
    [
        pytest.param(
            "mock_stromleser_device", "mock_stromleser_config_entry", id="stromleser"
        ),
        pytest.param(
            "mock_gasleser_device", "mock_gasleser_config_entry", id="gasleser"
        ),
        pytest.param(
            "mock_gasleser_pulse_device",
            "mock_gasleser_pulse_config_entry",
            id="gasleser_pulse",
        ),
        pytest.param(
            "mock_waermeleser_device", "mock_waermeleser_config_entry", id="waermeleser"
        ),
        pytest.param(
            "mock_wasserleser_device", "mock_wasserleser_config_entry", id="wasserleser"
        ),
    ],
)
async def test_device_sensors(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_energieleser_client: AsyncMock,
    request: pytest.FixtureRequest,
    device_fixture: str,
    config_entry_fixture: str,
) -> None:
    """Test all device family sensors against snapshots."""
    device = request.getfixturevalue(device_fixture)
    config_entry: MockConfigEntry = request.getfixturevalue(config_entry_fixture)
    mock_energieleser_client.get_device.return_value = device
    await _setup_integration(hass, config_entry)
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
