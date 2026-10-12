from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    width: int = 64
    height: int = 64
    dt: float = 0.12
    viscosity: float = 0.08
    diffusion: float = 0.03
