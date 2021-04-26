"""Support for Tibber notifications."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable
import logging
from typing import Any, Callable

from homeassistant.components.notify import (
    ATTR_TITLE,
    ATTR_TITLE_DEFAULT,
    BaseNotificationService,
)
from homeassistant.core import HomeAssistant

from . import DOMAIN as TIBBER_DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_get_service(
    hass: HomeAssistant,
    config: dict[str, Any],
    discovery_info: dict[str, Any] | None = None,
) -> TibberNotificationService:
    """Get the Tibber notification service."""
    tibber_connection = hass.data[TIBBER_DOMAIN]
    return TibberNotificationService(tibber_connection.send_notification)


class TibberNotificationService(BaseNotificationService):
    """Implement the notification service for Tibber."""

    def __init__(self, notify: Callable[..., Awaitable[None]]) -> None:
        """Initialize the service."""
        self._notify = notify

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a message to Tibber devices."""
        title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
        try:
            await self._notify(title=title, message=message)
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout sending message with Tibber")
