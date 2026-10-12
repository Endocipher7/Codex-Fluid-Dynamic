from pathlib import Path

from codex_fluid_dynamic import (
    FluidField,
    IonFieldProjection,
    MaterialSpec,
    render_scene,
)


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    fluid = FluidField(
        width=64,
        height=64,
        viscosity=0.08,
        diffusion=0.03,
        dt=0.12,
    )

    ion_field = IonFieldProjection(
        width=64,
        height=64,
        particle_count=120,
        strength=1.2,
        damping=0.94,
        spring_constant=0.06,
    )

    material = MaterialSpec(
        name="Mesogenic silica membrane",
        porosity=0.36,
        refractive_index=1.62,
        thermal_conductivity=0.82,
        anisotropy=0.27,
        transmission_floor=0.18,
    )

    for _ in range(30):
        fluid.step()
        ion_field.step(dt=0.12)

    output_path = output_dir / "scene.png"
    render_scene(
        fluid=fluid,
        ion_field=ion_field,
        material=material,
        path=str(output_path),
    )

    print(f"Rendered scene to {output_path.resolve()}")


if __name__ == "__main__":
    main()
