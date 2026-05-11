# Agent Notes

## Repo Overview
Personal learning repo for constraint programming and logic puzzles. Two independent Python sub-projects with no formal packaging or test suite.

## Structure

- `Kanren/` — Logic programming puzzles using `kanren` + local `logicpuzzles` helpers.
- `ORTools/` — OR-Tools CP-SAT examples and exercises. `ejemplos_ortools.py` is the main reference/cheatsheet.

## Running Code

Scripts are standalone; run individually:

```bash
python ORTools/pt1/pt1_lvl1.py
python Kanren/baron1.py
```

There is no central `main.py`, `setup.py`, or test runner. The root `README.md` references a non-existent `main.py` — ignore it.

## Dependencies

Install globally or in a venv as needed:

```bash
pip install ortools numpy kanren
```

- `ortools` — required for everything under `ORTools/`.
- `numpy` — used in some OR-Tools scripts.
- `kanren` — required for everything under `Kanren/`.

A `.venv` exists inside `ORTools/pt1/` but there is no root-level virtual environment.

## Conventions

- Comments and variable names are in **Spanish** throughout.
- Files with `_*` suffix (e.g., `baron10_.py`) are alternate or draft versions of the base file.
- `Kanren/logicpuzzles.py` is a shared helper module imported by most `baron*.py` scripts. There is a near-identical copy at `Kanren/more/logicpuzzles.py` (differs only by trailing newline).
- `ORTools/ejemplos_ortools.py` is a structured reference based on the included PDFs (`Metodos_OrTools.pdf`, `ortools_cheatsheet_grok.pdf`, `otools_cheatsheet_deepseek.pdf`). Treat it as the canonical API guide for this repo.
- `ORTools/pt1/pt1_data_model.py` is a documentation note (not executable) explaining why variables from different `CpModel` instances cannot be mixed.
- No CI, linting, formatting, or type-checking config exists.

## Gotchas

- **Do not mix variables from different `cp_model.CpModel()` instances** — OR-Tools will raise an error because variables are bound to their parent model by internal index.
- **Most scripts print directly on import** (no `if __name__ == "__main__":` guard). All `Kanren/baron*.py` files, all `Kanren/more/` files, most `ORTools/pt*` files, and most `ORTools/more/` files execute at module level. Only `ORTools/ejercicios/`, `ORTools/ejercicios_practica/`, and `ejemplos_ortools.py` have guards.
