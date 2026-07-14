# COCSOS for CEC2017 Benchmark Optimization — Problem 2

This repository provides the Python implementation of the **COCSOS** algorithm used for the **CEC2017 benchmark-function experiment** associated with the paper:

> **Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant**

## Authors

- Tuan Khanh Dang
- Nhat Huy Huynh
- Khoa Hoang Truong
- Dieu Ngoc Vo — Corresponding author

---

## 1. Overview

This code evaluates the proposed **COCSOS** algorithm on functions from the **CEC2017 benchmark suite**.

---

## 2. Current Default Configuration

The supplied script currently uses the following settings:

| Item | Default value |
|---|---:|
| Algorithm | COCSOS |
| Benchmark suite | CEC2017 |
| Active function group | `cec2017.simple` |
| Dimension | 100 |
| Search bounds | `[-100, 100]` |
| Independent runs | 30 |
| Population size | 50 |
| Maximum iterations | 1000 |
| CO application probability | 0.4 |
| Chaotic local-search trials | 20 |
| Output prefix | `COCSOS_CEC2017_F1-F10_100dim` |

---

## 5. Requirements

Recommended environment:

- Python 3.9 or later
- NumPy
- Pandas
- Matplotlib
- SciPy
- OpenPyXL
- a compatible local implementation of the `cec2017` package

---


## 7. How to Run the Default Experiment

Open a terminal in the directory containing the source file.

### Windows

```bash
python COCSOS_CEC2017.py
```

At startup, the script prints the names of all loaded benchmark functions:

```text
Danh sách các hàm benchmark đã load:
simple_f1
simple_f2
...
```

The program then executes:

```text
30 independent runs × all active CEC2017 functions
```

For each function, the terminal displays:

```text
Running Function: simple_f1 (Run 1) | Seed = ...
Iteration 100: Best fitness = ...
...
Algorithm finished in ... seconds.
```

---

## 8. Main Execution Block

The default configuration is controlled by:

```python
if __name__ == "__main__":
    max_iter = 1000
    common_bound = (-100, 100)
    dim = 100

    # Load CEC2017 functions here.

    run_multiple_times(
        functions,
        n_runs=30,
        pop_size=50,
        max_iter=max_iter
    )
```
---

## 9. Running Different Dimensions

### 10-dimensional experiment

```python
dim = 10

run_multiple_times(
    functions,
    n_runs=10,
    pop_size=50,
    max_iter=1000,
    excel_filename_prefix="COCSOS_CEC2017_F1-F10_10dim",
)
```
---

## 10. Activating the CEC2017 Function Groups

### 10.1 Simple functions

The following block is active by default:

```python
from cec2017.simple import all_functions as simple_functions

global_mins_simple = [0] * len(simple_functions)

for i, f in enumerate(simple_functions):
    func_name = f"simple_f{i+1}"
    wrapped_func = lambda x, f=f: f(x.reshape(1, -1))[0]
    functions[func_name] = (
        wrapped_func,
        common_bound,
        global_mins_simple[i],
        dim
    )
```

### 10.2 Hybrid functions

Uncomment the hybrid block:

```python
from cec2017.hybrid import all_functions as hybrid_functions

global_mins_hybrid = [0] * len(hybrid_functions)

for i, f in enumerate(hybrid_functions):
    func_name = f"hybrid_f{i+1}"
    wrapped_func = lambda x, f=f: f(x.reshape(1, -1))[0]
    functions[func_name] = (
        wrapped_func,
        common_bound,
        global_mins_hybrid[i],
        dim
    )
```

### 10.3 Composition functions

Uncomment the composition block:

```python
from cec2017.composition import all_functions as composition_functions

global_mins_composition = [0] * len(composition_functions)

for i, f in enumerate(composition_functions):
    func_name = f"composition_f{i+1}"
    wrapped_func = lambda x, f=f: f(x.reshape(1, -1))[0]
    functions[func_name] = (
        wrapped_func,
        common_bound,
        global_mins_composition[i],
        dim
    )
```

### 10.4 Running all available groups

When all groups are activated, use a matching output prefix:

```python
run_multiple_times(
    functions,
    n_runs=30,
    pop_size=50,
    max_iter=1000,
    excel_filename_prefix="COCSOS_CEC2017_F1-F30_10dim",
)
```

The exact number of functions depends on the imported `cec2017` package.

---

## 12. Random-Seed Protocol

The script creates one seed for each:

```text
Run + Function
```

Before every optimization run, it resets both random generators:

```python
np.random.seed(seed)
random.seed(seed)
```

The seed is stored in the Excel output and can be reused by SOS or another algorithm.

### Important reproducibility limitation

The seed table is currently created with:

```python
rng = np.random.default_rng()
```

without a fixed master seed.

Therefore:

- each complete execution generates a new seed table;
- the saved Excel seed table is required to reproduce the published experiment;
- rerunning the current script from the beginning does not recreate the same table automatically.

For complete experiment-level reproducibility, either:

1. publish the generated `Function_Seeds` sheet; or
2. modify the code to use a documented master seed:

```python
rng = np.random.default_rng(2026)
```

Do not regenerate the seed table when comparing COCSOS with SOS. The comparison algorithm must read the exact saved table.

## 14. Output Files

### 14.1 One workbook for each run

The default naming format is:

```text
COCSOS_CEC2017_F1-F10_100dim_1.xlsx
COCSOS_CEC2017_F1-F10_100dim_2.xlsx
...
COCSOS_CEC2017_F1-F10_100dim_30.xlsx
```

Each workbook contains:

- `Summary`;
- `Seed_Protocol`;
- `Experiment_Info`;
- one `*_InitOF` sheet for each active function;
- one convergence-history sheet for each active function.

### 14.2 Combined summary workbook

After all runs are completed, the script creates:

```text
COCSOS_CEC2017_F1-F10_100dim_ALL_SUMMARY.xlsx
```

This workbook contains:

- `All_Summary`;
- `Seed_Protocol`;
- `Function_Seeds`;
- `Run_Function_Seeds`;
- `Experiment_Info`.

---

## 15. Excel Sheet Descriptions

### `Summary`

Contains one row for every active function in the current run:

| Column | Description |
|---|---|
| Algorithm | Algorithm name |
| Run | Independent-run index |
| Function | CEC2017 function identifier |
| Seed | Seed assigned to the `Run–Function` pair |
| Dimension | Number of decision variables |
| Bounds | Search interval |
| Pop Size | Population size |
| Max Iter | Maximum iterations |
| Initial Best Index | One-based index of the best initial organism |
| Initial Best OF | Best objective value before CO |
| Initial Best Individual | Best initial decision vector |
| Best Solution | Final best decision vector |
| Best Fitness | Final best objective value |
| Theoretical Global Min | Reference minimum entered in the code |
| Running Time (s) | Elapsed optimization time |

### `Seed_Protocol`

Records the seed and experiment settings for every function in the current run.

### `Experiment_Info`

Describes:

- algorithm name;
- benchmark suite;
- number of runs;
- population size;
- maximum iterations;
- seed source;
- seed protocol;
- random libraries reset;
- initial-population recording;
- reproducibility conditions.

### `<function>_InitOF`

Stores:

- run number;
- function name;
- seed;
- organism index;
- initial objective value;
- all decision variables `x1, x2, ..., xD`.

### `<function>`

Stores the convergence history:

| Iteration | Meaning |
|---:|---|
| 0 | Best fitness in the original random population before CO |
| 1 | Best fitness after iteration 1 |
| ... | ... |
| 1000 | Final best fitness |

### `Function_Seeds`

This is the primary table to be reused by SOS or other comparison algorithms.


## 17. Calling COCSOS Directly

The optimizer can be called independently of the Excel experiment runner:

```python
best_solution, best_fitness, runtime, history, initial_info = COCSOS(
    obj_func=wrapped_func,
    bounds=(-100, 100),
    dim=100,
    pop_size=50,
    max_iter=1000,
    seed=123456789,
)
```

Returned objects:

| Output | Description |
|---|---|
| `best_solution` | Final best vector |
| `best_fitness` | Final best objective value |
| `runtime` | Elapsed time in seconds |
| `history` | Best-fitness sequence from iteration 0 onward |
| `initial_info` | Seed, initial population, initial objective values, and initial best organism |

Example:

```python
print("Best fitness:", best_fitness)
print("Best solution:", best_solution)
print("Runtime:", runtime)
```

---

## 23. Citation

When using this code, please cite the associated paper:

```bibtex
@article{Dang_COCSOS_DOCR,
  title   = {Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant},
  author  = {Dang, Tuan Khanh and Huynh, Nhat Huy and Truong, Khoa Hoang and Vo, Dieu Ngoc},
  journal = {Applied Soft Computing},
  year    = {[Year]},
  volume  = {[Volume]},
  pages   = {[Article number]},
  doi     = {[DOI]}
}
```
---

## 25. Contact

For questions regarding the code, seed protocol, or reproduction of the CEC2017 results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---
