from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class IonParticle:
    position: np.ndarray
    velocity: np.ndarray
    charge: float
    mass: float = 1.0
    damping: float = 0.96


class IonFieldProjection:
    """
    Simplified particle-field model approximating an ion projection matrix.
    This is not a real plasma physics solver, but it provides a coherent
    simulation layer for high-level projection and rendering.
    """

    def __init__(
        self,
        width: int = 64,
        height: int = 64,
        particle_count: int = 120,
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
        self.particles: list[IonParticle] = []

        for _ in range(particle_count):
            pos = rng.uniform(low=0.0, high=1.0, size=2)
            vel = rng.normal(0.0, 0.08, size=2)
            charge = rng.uniform(0.5, 1.5)
            self.particles.append(
                IonParticle(
                    position=pos,
                    velocity=vel,
                    charge=charge,
                    mass=rng.uniform(0.8, 1.6),
                    damping=damping,
                )
            )

    def _field_vector(self, pos: np.ndarray) -> np.ndarray:
        cx = (pos[0] - 0.5) * 2.0
        cy = (pos[1] - 0.5) * 2.0
        return np.array([
            -self.spring_constant * cx,
            -self.spring_constant * cy,
        ], dtype=np.float64)

    def step(self, dt: float = 0.12) -> None:
        for particle in self.particles:
            force = self._field_vector(particle.position) + np.array([
                self.strength * np.sin(particle.position[1] * 12.0 + particle.position[0] * 5.0),
                self.strength * np.cos(particle.position[0] * 10.0 + particle.position[1] * 6.0),
            ], dtype=np.float64)

            particle.velocity += (force / particle.mass) * dt
            particle.velocity *= particle.damping

            particle.position += particle.velocity * dt

            particle.position = np.clip(particle.position, 0.0, 1.0)

    def build_intensity_field(self) -> np.ndarray:
        field = np.zeros((self.height, self.width), dtype=np.float64)

        for particle in self.particles:
            x = int(np.clip(particle.position[0] * (self.width - 1), 0, self.width - 1))
            y = int(np.clip(particle.position[1] * (self.height - 1), 0, self.height - 1))
            field[y, x] += particle.charge * self.strength

        return field
