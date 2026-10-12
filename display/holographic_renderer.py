"""Display layer for holographic visualization."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class HolographicRenderer:
    """Simple renderer for fluid density, ion intensity, and projected display response."""

    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render(self, fluid_field, ion_field, material, filename: str = "scene.png") -> str:
        intensity = ion_field.intensity_map()
        optical = material.optical_response()

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f"{material.name} // transmission={optical['transmission']:.2f}")

        axes[0].imshow(fluid_field.as_array(), cmap="twilight_shifted")
        axes[0].set_title("Fluid Density")
        axes[0].axis("off")

        axes[1].imshow(intensity, cmap="plasma")
        axes[1].set_title("Ion Field Intensity")
        axes[1].axis("off")

        response = 0.4 + 0.6 * (fluid_field.as_array() + intensity / intensity.max() if intensity.max() > 0 else fluid_field.as_array())
        axes[2].imshow(response, cmap="viridis")
        axes[2].set_title("Display Projection")
        axes[2].axis("off")

        output_path = self.output_dir / filename
        plt.tight_layout()
        fig.savefig(output_path, dpi=200)
        plt.close(fig)
        return str(output_path)
