"""Module-level integration entrypoint for the Codex Fluid Dynamic simulation stack."""

from __future__ import annotations

from codex_fluid_dynamic import FluidField, IonFieldProjection, MaterialSpec, render_scene
from codex_fluid_dynamic.display import render_scene as _render_scene
from codex_fluid_dynamic.fluid import FluidField as _FluidField
from codex_fluid_dynamic.ion_field import IonFieldProjection as _IonFieldProjection
from codex_fluid_dynamic.materials import MaterialSpec as _MaterialSpec


class IntegratedSimulation:
    """High-level orchestrator connecting the fluid, ion, material, and display layers."""

    def __init__(
        self,
        width: int = 64,
        height: int = 64,
        steps: int = 30,
    ) -> None:
        self.fluid = FluidField(width=width, height=height)
        self.ion_field = IonFieldProjection(width=width, height=height)
        self.material = MaterialSpec(
            name="Mesogenic silica membrane",
            porosity=0.36,
            refractive_index=1.62,
            thermal_conductivity=0.82,
            anisotropy=0.27,
            transmission_floor=0.18,
        )
        self.steps = steps

    def run(self, path: str = "output/scene.png") -> str:
        for _ in range(self.steps):
            self.fluid.step()
            self.ion_field.step(dt=0.12)
        return render_scene(self.fluid, self.ion_field, self.material, path=path)
