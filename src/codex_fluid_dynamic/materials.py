from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class MaterialSpec:
    name: str
    porosity: float
    refractive_index: float
    thermal_conductivity: float
    anisotropy: float
    transmission_floor: float = 0.15

    def optical_response(self, wavelength_nm: float = 550.0, temperature_c: float = 22.0) -> dict:
        """
        Returns a simple optical response model for a mesogenic silica membrane.
        """
        wavelength_factor = 1.0 / max(wavelength_nm, 1.0)
        temperature_shift = (temperature_c / 100.0) * 0.015
        phase_shift = self.refractive_index * (1.0 + self.anisotropy) + temperature_shift

        transmission = 1.0 - (self.porosity * 0.7) - abs(self.anisotropy) * 0.3
        transmission = max(self.transmission_floor, transmission)
        attenuation = max(0.02, 1.0 - transmission)

        return {
            "refractive_index": float(self.refractive_index + temperature_shift),
            "phase_shift": float(phase_shift),
            "transmission": float(transmission),
            "attenuation": float(attenuation),
            "wavelength_factor": float(wavelength_factor),
            "thermal_conductivity": float(self.thermal_conductivity),
        }
