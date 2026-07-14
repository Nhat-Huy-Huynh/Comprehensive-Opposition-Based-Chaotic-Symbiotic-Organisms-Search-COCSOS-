# COCSOS for Benchmark Optimization — Problem 1

This repository provides the Python implementation of the **COCSOS** algorithm used in the benchmark-function experiment associated with the paper:

> **Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant**

## Authors

- Tuan Khanh Dang
- Nhat Huy Huynh
- Khoa Hoang Truong
- Dieu Ngoc Vo — Corresponding author

---

## 1. Purpose of this code

This program evaluates the proposed **COCSOS** algorithm on continuous benchmark functions. It supports:

- repeated independent runs;
- one recorded random seed for each `Run–Function` pair;
- export of the initial random population and its objective values;
- export of convergence history;
- export of the best solution, best fitness, and runtime;
- generation of an Excel seed table that can later be reused by the original SOS algorithm for a fair comparison.

The current script is configured to run **Benchmark Problem 1 only**, namely the shifted **Styblinski–Tang** function.

---

## 2. Current experiment configuration

The active configuration in the supplied code is:

| Item | Current value |
|---|---:|
| Algorithm | COCSOS |
| Benchmark function | Styblinski–Tang |
| Dimension | 50 |
| Lower bound | -5 |
| Upper bound | 5 |
| Theoretical global minimum | 0 |
| Population size | 50 |
| Maximum iterations | 1000 |
| Independent runs | 50 |
| Chaotic local-search limit | 20 |
| Probability of applying the CO phase | 0.4 |
| Output prefix | `COCSOS_runs_seed_protocol_50dim` |

The shifted function implemented in the code is:

\[
f(\mathbf{x}) =
39.16616572302271D
+
\frac{1}{2}
\sum_{i=1}^{D}
\left(x_i^4-16x_i^2+5x_i\right),
\]

where \(D=50\). The additive offset shifts the known global minimum to approximately zero.

---

## 3. Algorithm components

The implementation combines the three original SOS interaction phases with two additional mechanisms.

### Original SOS phases

1. Mutualism
2. Commensalism
3. Parasitism

### Additional COCSOS mechanisms

- **Comprehensive Opposition (CO)**  
  Generates alternative organisms using REO, QR, QO, or EO strategies. The strategy probabilities change according to the iteration ratio.

- **Chaotic Local Search (CLS)**  
  Uses a logistic map and population-based perturbation around the current best solution.

All generated solutions are clipped to the specified lower and upper bounds.

---

## 4. File preparation

Place the Python source file in the repository root and rename it to a descriptive filename, for example:

```text
COCSOS_Benchmark_Problem1.py
```

Recommended directory:

```text
COCSOS-Benchmark-Problem1/
├── COCSOS_Benchmark_Problem1.py
├── README.md
└── requirements.txt
```

A larger reproducibility repository may use:

```text
COCSOS-Benchmark-Problem1/
├── src/
│   └── COCSOS_Benchmark_Problem1.py
├── results/
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 5. Software requirements

Recommended environment:

- Python 3.9 or later
- NumPy
- Pandas
- SciPy
- OpenPyXL

Install the required packages with:

```bash
pip install numpy pandas scipy openpyxl
```

A suitable `requirements.txt` is:

```text
numpy
pandas
scipy
openpyxl
```

> `scipy.stats.qmc` and `math` are imported in the current script but are not used by the active experiment.

---

## 6. How to run

Open a terminal in the folder containing the Python file.

### Windows

```bash
python COCSOS_Benchmark_Problem1.py
```

### Linux or macOS

```bash
python3 COCSOS_Benchmark_Problem1.py
```

The script automatically:

1. creates a seed table;
2. runs the active benchmark function 50 times;
3. resets both NumPy and Python random generators before each run;
4. stores detailed results for every run;
5. creates one combined summary workbook.

During execution, the terminal prints information such as:

```text
========== COCSOS Run 1/50 ==========
Running function: styblinski_tang | Run = 1 | Seed = ...
Iteration 100: Best fitness = ...
...
Algorithm finished in ... seconds.
```

---

## 7. Output files

### 7.1 Individual-run workbooks

For each run, the program creates:

```text
COCSOS_runs_seed_protocol_50dim_run_1.xlsx
COCSOS_runs_seed_protocol_50dim_run_2.xlsx
...
COCSOS_runs_seed_protocol_50dim_run_50.xlsx
```

Each workbook contains the following sheets.

#### `Summary`

Stores:

- algorithm name;
- run number;
- benchmark name;
- random seed;
- dimension and bounds;
- population size;
- maximum iterations;
- best initial organism;
- best initial objective value;
- final best solution;
- final best fitness;
- theoretical global minimum;
- elapsed runtime.

#### `Seed_Protocol`

Stores the seed and experiment settings for the current run and function.

#### `Experiment_Info`

Describes the number of runs, population size, maximum iterations, seed protocol, and random libraries that are reset.

#### `styblinski_tang_InitOF`

Stores the complete initial random population:

- 50 organisms;
- 50 decision variables per organism;
- initial objective value of every organism;
- run number;
- function name;
- seed.

#### `styblinski_tang`

Stores the convergence history:

| Iteration | Best Fitness |
|---:|---:|
| 0 | Best fitness of the random initial population |
| 1 | Best fitness after iteration 1 |
| ... | ... |
| 1000 | Final best fitness |

---

### 7.2 Combined summary workbook

After all runs are completed, the script creates:

```text
COCSOS_runs_seed_protocol_50dim_ALL_SUMMARY.xlsx
```

This workbook contains:

- `All_Summary`
- `Seed_Protocol`
- `Function_Seeds`
- `Run_Function_Seeds`
- `Experiment_Info`

The `Function_Seeds` sheet is the main seed table intended for reuse by the original SOS algorithm.

---

## 8. Random-seed protocol

For every `Run–Function` pair, the program generates one integer seed and then resets:

```python
np.random.seed(seed)
random.seed(seed)
```

This ensures that all stochastic operations inside one COCSOS run are controlled by the recorded seed.

### Important reproducibility note

The function `make_function_seed_table()` currently uses:

```python
rng = np.random.default_rng()
```

without a fixed master seed. Therefore:

- every new execution of the complete script creates a new seed table;
- the results are reproducible only when the saved seed table is retained;
- rerunning the current script from the beginning does not automatically recreate the same seed table.

For a fair COCSOS–SOS comparison, the SOS implementation should read the exact seeds from:

```text
COCSOS_runs_seed_protocol_50dim_ALL_SUMMARY.xlsx
Sheet: Function_Seeds
```

and use the seed corresponding to the same run and function.

For full experiment-level reproducibility, either:

1. preserve and publish the generated `Function_Seeds` sheet; or
2. modify the seed-table generator to use a documented master seed.

---

## 9. Initial population and fair comparison

For a fixed combination of:

- function;
- run;
- seed;
- dimension;
- bounds;
- population size;
- NumPy random-number implementation;

the random initial population is generated by:

```python
pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
```

The initial population is saved before the first Comprehensive Opposition operation.

Therefore, SOS can reproduce the same random initial population by:

1. reading the same seed;
2. resetting both random libraries;
3. using the same bounds, dimension, and population size;
4. generating the population before making any other random call.

The per-run `*_InitOF` sheet allows users to verify the complete initial population and all initial objective values directly.

---

## 10. Changing the number of runs or algorithm settings

Edit the main block:

```python
if __name__ == "__main__":
    excel_filename_prefix = "COCSOS_runs_seed_protocol_50dim"

    run_all_benchmarks_excel(
        excel_filename_prefix,
        num_runs=50,
        pop_size=50,
        max_iter=1000,
    )
```

Examples:

### Ten test runs

```python
run_all_benchmarks_excel(
    excel_filename_prefix,
    num_runs=10,
    pop_size=50,
    max_iter=1000,
)
```

### Population size of 100

```python
run_all_benchmarks_excel(
    excel_filename_prefix,
    num_runs=50,
    pop_size=100,
    max_iter=1000,
)
```

### Maximum of 2000 iterations

```python
run_all_benchmarks_excel(
    excel_filename_prefix,
    num_runs=50,
    pop_size=50,
    max_iter=2000,
)
```

Update the output prefix whenever the experiment configuration changes, for example:

```python
excel_filename_prefix = "COCSOS_StyblinskiTang_50D_N100_T2000"
```

---

## 11. Activating another benchmark function

The active functions are controlled by the `functions` dictionary.

Current configuration:

```python
functions = {
    "styblinski_tang": (
        styblinski_tang_function,
        [-5, 5],
        0,
        50
    )
}
```

Each entry follows this format:

```python
"function_name": (
    objective_function,
    [lower_bound, upper_bound],
    theoretical_global_minimum,
    dimension
)
```

For example, to run the 30-dimensional Ackley function:

```python
functions = {
    "ackley": (
        ackley_function,
        [-100, 100],
        0,
        30
    )
}
```

To run several functions in the same experiment:

```python
functions = {
    "ackley": (ackley_function, [-100, 100], 0, 30),
    "sphere": (sphere_function, [-100, 100], 0, 30),
    "styblinski_tang": (styblinski_tang_function, [-5, 5], 0, 30),
}
```

When several functions are active, the script assigns a separate seed to every `Run–Function` pair and creates separate initialization and convergence sheets.

---

## 12. Adding a new benchmark function

Define the objective function:

```python
def new_benchmark_function(x):
    x = np.asarray(x)
    return np.sum(x**2)
```

Then add it to the dictionary:

```python
functions = {
    "new_benchmark": (
        new_benchmark_function,
        [-100, 100],
        0,
        30
    )
}
```

The objective function must:

- accept a one-dimensional NumPy array;
- return one scalar fitness value;
- follow a minimization formulation;
- be valid over the declared search bounds.

---

## 13. Using the COCSOS function independently

The optimizer can also be called directly:

```python
best_solution, best_fitness, runtime, history, initial_info = COCSOS(
    obj_func=styblinski_tang_function,
    bounds=[-5, 5],
    dim=50,
    pop_size=50,
    max_iter=1000,
    seed=123456789,
)
```

Returned objects:

| Output | Description |
|---|---|
| `best_solution` | Final best decision vector |
| `best_fitness` | Final best objective value |
| `runtime` | Elapsed time in seconds |
| `history` | Best-fitness sequence from iteration 0 to the final iteration |
| `initial_info` | Seed, complete initial population, initial objective values, and initial best organism |

Example:

```python
print("Best fitness:", best_fitness)
print("Best solution:", best_solution)
print("Runtime:", runtime)
```

---

## 14. Computational considerations

The default experiment performs:

```text
50 independent runs × 1000 iterations
```

for a population of 50 organisms. Each iteration contains:

- mutualism updates;
- commensalism updates;
- parasitism updates;
- optional CO population generation;
- 20 chaotic local-search trials.

Execution time depends on:

- CPU performance;
- Python and NumPy versions;
- number and dimension of active functions;
- population size;
- maximum iterations;
- Excel-writing speed.

The code executes runs sequentially and does not use multiprocessing.

---

## 15. Recommended publication package

For public release, include:

```text
COCSOS-Benchmark-Problem1/
├── COCSOS_Benchmark_Problem1.py
├── README.md
├── requirements.txt
├── LICENSE
├── results/
│   └── COCSOS_runs_seed_protocol_50dim_ALL_SUMMARY.xlsx
└── sample_output/
    └── COCSOS_runs_seed_protocol_50dim_run_1.xlsx
```

For complete reproducibility, also publish all per-run workbooks or an equivalent compressed data package.

---

## 16. Citation

When this code is used, please cite the associated paper:

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

After the software is archived on Zenodo, add the software citation:

```bibtex
@software{Dang_COCSOS_Benchmark_Code,
  author  = {Dang, Tuan Khanh and Huynh, Nhat Huy and Truong, Khoa Hoang and Vo, Dieu Ngoc},
  title   = {COCSOS source code for benchmark-function optimization},
  year    = {[Year]},
  version = {1.0.0},
  doi     = {[Software DOI]}
}
```

---

## 17. License

Add the selected open-source license before public release.

Recommended options:

- MIT License;
- BSD 3-Clause License;
- GNU GPL-3.0.

Do not publish the repository without a clear license if reuse and redistribution are intended.

---

## 18. Contact

For questions regarding the code, experimental protocol, or reproduction of the benchmark results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---

## 19. Notes

- The current script minimizes all benchmark functions.
- The current active experiment is Styblinski–Tang at 50 dimensions.
- The initial best index is stored in Excel using one-based numbering.
- The convergence history starts at iteration 0 with the best fitness of the random initial population.
- The CO population used by COCSOS is generated after the random initial population has been recorded.
- Excel sheet names are automatically sanitized and truncated to satisfy the 31-character Excel limit.
- The output files are written to the current working directory unless a path is included in `excel_filename_prefix`.