from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .fluid import FluidField
from .ion_field import IonFieldProjection
from .materials import MaterialSpec


def render_scene(
    fluid: FluidField,
    ion_field: IonFieldProjection,
    material: MaterialSpec,
    path: str = "output/scene.png",
) -> str:
    intensity = ion_field.build_intensity_field()
    optical = material.optical_response()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"{material.name} // transmission={optical['transmission']:.2f}")

    axes[0].imshow(fluid.density, cmap="twilight_shifted")
    axes[0].set_title("Fluid Density")
    axes[0].axis("off")

    axes[1].imshow(intensity, cmap="plasma")
    axes[1].set_title("Ion Field Intensity")
    axes[1].axis("off")

    response = 0.4 + 0.6 * (fluid.density + intensity / intensity.max() if intensity.max() > 0 else 0)
    axes[2].imshow(response, cmap="viridis")
    axes[2].set_title("Display Projection")
    axes[2].axis("off")

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)

    return str(output)
