# Codex Fluid Dynamic

A prototype multi-layer simulation and visualization stack for a fluidic, ion-projection, and holographic display system.

## Overview

This project combines:
- a simplified fluid simulation layer
- an ion field projection model
- a material optical response model
- a renderer for visualization

This is a science-leaning prototype designed to be extended with more physically accurate numerical methods and hardware control logic.

## Live concept

The repository is structured around a multi-layer system inspired by the following conceptual stack:

1. Sensing Layer
2. Material Layer
3. Ion Field Layer
4. Simulation Layer
5. Display Layer

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The script writes a rendered output to `output/scene.png`.

## Repository structure

- `src/codex_fluid_dynamic/fluid.py` - fluid simulation
- `src/codex_fluid_dynamic/ion_field.py` - ion projection model
- `src/codex_fluid_dynamic/materials.py` - material properties and optical response
- `src/codex_fluid_dynamic/display.py` - visualization
- `app.py` - demo entrypoint

## Extending the project

Suggested next steps:
- replace the simplified fluid solver with a higher-order CFD model
- connect ion field projection to a real hardware control layer
- integrate ARTIQ pulse sequence logic
- add a web app or interactive dashboard for live simulation
- generate animation frames for an immersive holographic display preview
