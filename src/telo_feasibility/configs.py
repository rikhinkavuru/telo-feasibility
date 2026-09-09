"""Loaders for the YAML configuration files under ``config/``.

Every loader validates through ``schemas`` so an inconsistent unit, an
out-of-range value, or a parameter without provenance fails here, at load time.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .provenance import GATES_PATH, PACKAGE_ROOT
from .schemas import (
    FROZEN_STRATEGY_IDS,
    GateSet,
    ParameterSet,
    ProductPresentation,
    StrategyDesign,
    StrategyId,
)

CONFIG_ROOT = PACKAGE_ROOT / "config"
GLOBAL_PATH = CONFIG_ROOT / "global.yaml"
PRODUCTS_DIR = CONFIG_ROOT / "products"
STRATEGIES_PATH = CONFIG_ROOT / "strategies" / "illustrative_baseline.yaml"
DESIGN_SPACE_STRATEGIES_PATH = CONFIG_ROOT / "strategies" / "design_space.yaml"


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return data


def load_parameter_set(path: Path) -> ParameterSet:
    return ParameterSet.model_validate(_read_yaml(path))


def load_global(path: Path = GLOBAL_PATH) -> ParameterSet:
    return load_parameter_set(path)


@dataclass(frozen=True)
class ProductConfig:
    presentation: ProductPresentation
    parameters: ParameterSet
    path: Path

    @property
    def id(self) -> str:
        return self.presentation.id


def load_product(path: Path) -> ProductConfig:
    raw = _read_yaml(path)
    pres = ProductPresentation.model_validate(raw["presentation"])
    params = ParameterSet.model_validate(raw["parameters"])
    if path.stem != pres.id:
        raise ValueError(f"{path.name}: filename stem must equal presentation id {pres.id!r}")
    if params.id != f"product.{pres.id}":
        raise ValueError(f"{path.name}: parameter set id must be 'product.{pres.id}'")
    return ProductConfig(presentation=pres, parameters=params, path=path)


def load_products(directory: Path = PRODUCTS_DIR) -> dict[str, ProductConfig]:
    out: dict[str, ProductConfig] = {}
    for p in sorted(directory.glob("*.yaml")):
        cfg = load_product(p)
        out[cfg.id] = cfg
    if not out:
        raise FileNotFoundError(f"no product configs under {directory}")
    return out


@dataclass(frozen=True)
class StrategySet:
    id: str
    description: str
    source_locator: str
    designs: list[StrategyDesign]

    def by_id(self, sid: StrategyId) -> StrategyDesign:
        for d in self.designs:
            if d.id is sid:
                return d
        raise KeyError(sid.value)


def load_strategies(path: Path = STRATEGIES_PATH) -> StrategySet:
    """The eight frozen protocol comparators S0-S7, in order."""
    raw = _read_yaml(path)
    designs = [StrategyDesign.model_validate(d) for d in raw["designs"]]
    ids = [d.id for d in designs]
    if ids != list(FROZEN_STRATEGY_IDS):
        raise ValueError(
            f"{path.name}: designs must be S0..S7 in order, got {[i.value for i in ids]}"
        )
    return StrategySet(
        id=str(raw["id"]),
        description=str(raw.get("description", "")),
        source_locator=str(raw.get("source_locator", "")),
        designs=designs,
    )


def load_design_space_strategies(path: Path = DESIGN_SPACE_STRATEGIES_PATH) -> StrategySet:
    """Design-space strategies S8+ (2026-09 assignment). An absent file means none."""
    if not path.is_file():
        return StrategySet(id="design_space", description="", source_locator="", designs=[])
    raw = _read_yaml(path)
    designs = [StrategyDesign.model_validate(d) for d in raw.get("designs", [])]
    ids = [d.id for d in designs]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path.name}: duplicate strategy ids")
    frozen = [i.value for i in ids if i.is_frozen]
    if frozen:
        raise ValueError(f"{path.name}: S0-S7 are frozen and may not be redefined: {frozen}")
    return StrategySet(
        id=str(raw.get("id", "design_space")),
        description=str(raw.get("description", "")),
        source_locator=str(raw.get("source_locator", "")),
        designs=designs,
    )


def load_all_strategies(
    frozen_path: Path = STRATEGIES_PATH, design_space_path: Path = DESIGN_SPACE_STRATEGIES_PATH
) -> StrategySet:
    """Frozen comparators followed by design-space strategies; one registry for every runner."""
    frozen = load_strategies(frozen_path)
    extra = load_design_space_strategies(design_space_path)
    return StrategySet(
        id="all",
        description=f"{frozen.id} + {extra.id}",
        source_locator=frozen.source_locator,
        designs=[*frozen.designs, *extra.designs],
    )


def load_gates(path: Path = GATES_PATH) -> GateSet:
    return GateSet.model_validate(_read_yaml(path))


@dataclass(frozen=True)
class IllustrativeCount:
    total_parameters: int
    illustrative: int
    missing: int
    by_set: dict[str, tuple[int, int]]

    @property
    def any_illustrative(self) -> bool:
        return self.illustrative > 0 or self.missing > 0


def count_illustrative(sets: list[ParameterSet]) -> IllustrativeCount:
    total = 0
    ill = 0
    miss = 0
    by_set: dict[str, tuple[int, int]] = {}
    for s in sets:
        n = len(s.parameters)
        i = len(s.illustrative_ids())
        m = len(s.missing_ids())
        total += n
        ill += i
        miss += m
        by_set[s.id] = (i + m, n)
    return IllustrativeCount(total_parameters=total, illustrative=ill, missing=miss, by_set=by_set)
