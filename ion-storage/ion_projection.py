"""Ion-field projection layer for the Codex-Fluid-Dynamic project."""

from __future__ import annotations

import numpy as np


class IonFieldProjection:
    """A reduced-order ion-field estimator for charge projection and field intensity."""

    def __init__(
        self,
        width: int = 64,
        height: int = 64,
        particle_count: int = 128,
        strength: float = 1.2,
        damping: float = 0.94,
        spring_constant: float = 0.06,
    ) -> None:
        self.width = width
        self.height = height
        self.strength = strength
        self.damping = damping
        self.spring_constant = spring_constant

        rng = np.random.default_rng(7)
        self.positions = rng.uniform(0.0, 1.0, size=(particle_count, 2))
        self.velocities = rng.normal(0.0, 0.08, size=(particle_count, 2))
        self.charges = rng.uniform(0.5, 1.5, size=particle_count)
        self.masses = rng.uniform(0.8, 1.6, size=particle_count)

    def _field_force(self, pos: np.ndarray) -> np.ndarray:
        cx = (pos[0] - 0.5) * 2.0
        cy = (pos[1] - 0.5) * 2.0
        return np.array([
            -self.spring_constant * cx,
            -self.spring_constant * cy,
        ], dtype=np.float64)

    def step(self, dt: float = 0.12) -> None:
        force_x = np.empty_like(self.velocities[:, 0])
        force_y = np.empty_like(self.velocities[:, 1])

        for i, pos in enumerate(self.positions):
            field_force = self._field_force(pos)
            harmonic = np.array([
                self.strength * np.sin(pos[1] * 12.0 + pos[0] * 5.0),
                self.strength * np.cos(pos[0] * 10.0 + pos[1] * 6.0),
            ], dtype=np.float64)
            total_force = field_force + harmonic
            self.velocities[i] += (total_force / self.masses[i]) * dt
            self.velocities[i] *= self.damping
            self.positions[i] += self.velocities[i] * dt
            self.positions[i] = np.clip(self.positions[i], 0.0, 1.0)

            force_x[i] = total_force[0]
            force_y[i] = total_force[1]

    def intensity_map(self) -> np.ndarray:
        field = np.zeros((self.height, self.width), dtype=np.float64)
        for pos, charge in zip(self.positions, self.charges):
            x = int(np.clip(pos[0] * (self.width - 1), 0, self.width - 1))
            y = int(np.clip(pos[1] * (self.height - 1), 0, self.height - 1))
            field[y, x] += charge * self.strength
        return field
