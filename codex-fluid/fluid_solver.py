"""Fluid simulation layer for the Codex-Fluid-Dynamic project."""

from __future__ import annotations

import numpy as np


class NavierStokes2D:
    """A lean 2D incompressible fluid field approximation for simulation and rendering."""

    def __init__(
        self,
        width: int = 64,
        height: int = 64,
        viscosity: float = 0.08,
        diffusion: float = 0.03,
        dt: float = 0.12,
    ) -> None:
        self.width = width
        self.height = height
        self.viscosity = viscosity
        self.diffusion = diffusion
        self.dt = dt

        rng = np.random.default_rng(42)
        self.density = rng.random((height, width), dtype=np.float64)
        self.velocity_x = rng.normal(0.0, 0.16, size=(height, width)).astype(np.float64)
        self.velocity_y = rng.normal(0.0, 0.16, size=(height, width)).astype(np.float64)

    def _laplace(self, field: np.ndarray) -> np.ndarray:
        return (
            np.roll(field, 1, axis=0)
            + np.roll(field, -1, axis=0)
            + np.roll(field, 1, axis=1)
            + np.roll(field, -1, axis=1)
            - 4.0 * field
        )

    def _grad_x(self, field: np.ndarray) -> np.ndarray:
        return (np.roll(field, -1, axis=1) - np.roll(field, 1, axis=1)) / 2.0

    def _grad_y(self, field: np.ndarray) -> np.ndarray:
        return (np.roll(field, -1, axis=0) - np.roll(field, 1, axis=0)) / 2.0

    def inject_force(self, cx: int, cy: int, radius: int = 4, magnitude: float = 0.2) -> None:
        yy, xx = np.indices((self.height, self.width))
        dist_sq = (xx - cx) ** 2 + (yy - cy) ** 2
        mask = dist_sq <= radius ** 2
        self.density[mask] = np.clip(self.density[mask] + magnitude, 0.0, 1.0)
        self.velocity_x[mask] += magnitude * 0.5
        self.velocity_y[mask] += magnitude * 0.5

    def step(self) -> None:
        lap_d = self._laplace(self.density)
        divergence = (
            self.velocity_x - np.roll(self.velocity_x, 1, axis=1)
            + self.velocity_y - np.roll(self.velocity_y, 1, axis=0)
        )

        self.density = np.clip(
            self.density
            + self.dt * (
                self.diffusion * lap_d
                - 0.35 * self._grad_x(self.density) * self.velocity_x
                - 0.35 * self._grad_y(self.density) * self.velocity_y
                - 0.25 * divergence
            ),
            0.0,
            1.0,
        )

        self.velocity_x += self.dt * (
            self.viscosity * self._laplace(self.velocity_x) - 0.8 * self._grad_x(self.density)
        )
        self.velocity_y += self.dt * (
            self.viscosity * self._laplace(self.velocity_y) - 0.8 * self._grad_y(self.density)
        )

        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

    def as_array(self) -> np.ndarray:
        return self.density.copy()
