from __future__ import annotations

import numpy as np


class FluidField:
    """
    Minimal fluid simulation approximating a 2D incompressible field
    using a finite-difference style advection/diffusion update.
    """

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
        self.velocity_x = rng.normal(0.0, 0.18, size=(height, width)).astype(np.float64)
        self.velocity_y = rng.normal(0.0, 0.18, size=(height, width)).astype(np.float64)

    def _laplace(self, field: np.ndarray) -> np.ndarray:
        lap = (
            np.roll(field, 1, axis=0)
            + np.roll(field, -1, axis=0)
            + np.roll(field, 1, axis=1)
            + np.roll(field, -1, axis=1)
            - 4.0 * field
        )
        return lap

    def _gradient_x(self, field: np.ndarray) -> np.ndarray:
        return (np.roll(field, -1, axis=1) - np.roll(field, 1, axis=1)) / 2.0

    def _gradient_y(self, field: np.ndarray) -> np.ndarray:
        return (np.roll(field, -1, axis=0) - np.roll(field, 1, axis=0)) / 2.0

    def add_source(self, cx: int, cy: int, radius: int = 4, force: float = 0.2) -> None:
        yy, xx = np.indices((self.height, self.width))
        dist2 = (xx - cx) ** 2 + (yy - cy) ** 2
        mask = dist2 <= radius ** 2
        self.density[mask] = np.clip(self.density[mask] + force, 0.0, 1.0)
        self.velocity_x[mask] += force * 0.5
        self.velocity_y[mask] += force * 0.5

    def step(self) -> None:
        lap_density = self._laplace(self.density)
        div = (
            self.velocity_x
            - np.roll(self.velocity_x, 1, axis=1)
            + self.velocity_y
            - np.roll(self.velocity_y, 1, axis=0)
        )

        self.density = np.clip(
            self.density
            + self.dt * (
                self.diffusion * lap_density
                - 0.35 * self._gradient_x(self.density) * self.velocity_x
                - 0.35 * self._gradient_y(self.density) * self.velocity_y
                - 0.25 * div
            ),
            0.0,
            1.0,
        )

        self.velocity_x += self.dt * (
            self.viscosity * self._laplace(self.velocity_x)
            - 0.8 * self._gradient_x(self.density)
        )
        self.velocity_y += self.dt * (
            self.viscosity * self._laplace(self.velocity_y)
            - 0.8 * self._gradient_y(self.density)
        )

        self.velocity_x *= 0.99
        self.velocity_y *= 0.99
