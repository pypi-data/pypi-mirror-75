__all__ = ["Seabreeze"]

import asyncio
from typing import Dict, Any, List

from seabreeze.spectrometers import Spectrometer  # type: ignore
from yaqd_core import Sensor, logging


class Seabreeze(Sensor):
    _kind = "seabreeze"

    def __init__(self, name, config, config_filepath):
        self.spec = Spectrometer.from_serial_number(config.get("serial"))

        super().__init__(name, config, config_filepath)

        self._correct_dark_counts = config.get("correct_dark_counts", False)
        self._correct_nonlinearity = config.get("correct_nonlinearity", False)

        self._channel_names = ["wavelengths", "intensities"]
        self._channel_units = {"wavelengths": "nm", "intensities": None}
        self._channel_shapes = {
            "wavelengths": (self.spec.pixels,),
            "intensities": (self.spec.pixels,),
        }

        self.set_integration_time_micros(self._state["integration_time_micros"])

    async def _measure(self):
        return {
            "wavelengths": self.spec.wavelengths(),
            "intensities": self.spec.intensities(
                self._correct_dark_counts, self._correct_nonlinearity
            ),
        }

    def set_integration_time_micros(self, micros: int) -> None:
        """Set the integration time in microseconds"""
        self._integration_time_micros = micros
        self.spec.integration_time_micros(micros)

    def get_integration_time_micros(self) -> int:
        """Get the integration time in microseconds"""
        return self._integration_time_micros
