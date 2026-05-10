# AGENTS.md — ORTools Learning Repo

Personal learning repository for Google OR-Tools CP-SAT. Standalone Python scripts, no build system.

## Run a script

```bash
python <script>.py
```

Most scripts are self-contained. `pt1/lvl3.py` depends on `pt1/lvl2_class_printer.py`; run from inside `pt1/`.

## Dependencies

- `ortools`
- `numpy`

A venv exists only under `pt1/.venv/` (Python 3.14). Prefer installing dependencies globally or creating a fresh venv at repo root.

## Repo layout

| Directory | Contents |
|-----------|----------|
| `pt1/` | CP-SAT basics: variables, constraints, feasible search, solution enumeration |
| `pt2/` | Optimization example (maximization) |
| `pt3/` | Duplicate/basic patterns (similar to pt1) |
| `pt4/` | Sudoku solver with CP-SAT |
| `more/` | Puzzle solvers: sudoku, nonogram, map coloring, kakurasu, rascacielos, cryptarithmetic, magic square |
| `ejemplos_ortools.py` | Comprehensive CP-SAT API cheatsheet / reference |

## Quirks

- **Language:** Comments and variable names are in Spanish.
- **API naming inconsistency:** OR-Tools accepts both `new_int_var` / `add_all_different` (snake_case) and `NewIntVar` / `AddAllDifferent` (camelCase). Files across the repo use both.
- **Callback casing inconsistency:** Some callbacks use `OnSolutionCallback` / `SolutionCount` (camelCase) and others use `on_solution_callback` / `solution_count` (snake_case). Match the style already present in the file you edit.
- **Numpy incompatibility:** `model.AddAutomaton()` is incompatible with NumPy arrays. Use plain Python lists instead (see `more/nonogram.py`).
- **No tests:** `test.py` at root is just a NumPy snippet, not a test suite.
