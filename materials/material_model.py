"""Material model layer for the Codex-Fluid-Dynamic project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MesogenicSilicaMembrane:
    name: str = "Mesogenic silica membrane"
    porosity: float = 0.36
    refractive_index: float = 1.62
    thermal_conductivity: float = 0.82
    anisotropy: float = 0.27
    transmission_floor: float = 0.18

    def optical_response(self, wavelength_nm: float = 550.0, temperature_c: float = 22.0) -> dict:
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

    def thermal_profile(self, temperature_c: float = 22.0) -> float:
        return max(0.0, 1.0 - abs(temperature_c - 25.0) / 100.0)
