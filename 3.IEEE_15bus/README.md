# COCSOS_Original
# COCSOS for Directional Overcurrent Relay Coordination — Problem 3

This repository contains the **COCSOS** implementation used for **Problem 3: directional overcurrent relay coordination in a 42-relay distribution network**.

The study evaluates five relay-characteristic cases:

1. **NI** — Normal Inverse  
2. **VI** — Very Inverse  
3. **EI** — Extremely Inverse  
4. **Adaptive** — optimized/adaptive inverse-time characteristic  
5. **Hybrid** — mixed characteristic assignment among relays  

The code is associated with the paper:

> **Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant**

## Authors

- Tuan Khanh Dang
- Nhat Huy Huynh
- Khoa Hoang Truong
- Dieu Ngoc Vo — Corresponding author

---

## 1. Important clarification

Although this experiment may be stored near the CEC2017 benchmark code in the project repository, the supplied source file is **not a CEC2017 benchmark program**. It solves a constrained relay-setting optimization problem using actual relay, fault-current, current-transformer, and primary–backup coordination data.

The uploaded source file currently implements the **EI case**, because its operating-time equation is:

```python
return TDS * (80 / (ratio**2 - 1))
```

and its output prefix contains:

```text
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol
```

The NI, VI, Adaptive, and Hybrid cases should be run using their corresponding source-code variants or by applying the characteristic definitions described below.

---

## 2. Problem description

The optimization problem contains:

| Item | Value |
|---|---:|
| Number of relays | 42 |
| Number of primary–backup pairs | 82 |
| Coordination time interval | 0.2 s |
| Fixed-case decision variables | 84 |
| TDS variables | 42 |
| PS variables | 42 |
| Population size | 50 |
| Maximum iterations | 5000 |
| Independent runs in the supplied code | 30 |
| CO application probability | 0.4 |
| CLS trial limit | 20 |

For fixed NI, VI, and EI characteristics, each organism has the structure:

\[
\mathbf{x}=
[TDS_1,\ldots,TDS_{42},PS_1,\ldots,PS_{42}]
\]

with a total dimension of:

\[
2D=84.
\]

The relay pickup current is calculated as:

\[
I_{\mathrm{pickup},i}=CT_i\,PS_i.
\]

---

## 3. Decision-variable bounds

The bounds actually used by the optimizer are:

| Variable | Lower bound | Upper bound |
|---|---:|---:|
| TDS | 0.1 | 1.1 |
| PS | 0.5 | 2.5 |

The code creates these bounds inside `COCSOS()`:

```python
lb = np.concatenate((
    np.array([bounds[0]] * D_local),
    np.array([0.5] * D_local)
))

ub = np.concatenate((
    np.array([bounds[1]] * D_local),
    np.array([2.5] * D_local)
))
```

The PS values are quantized to five decimal places:

```python
ps_quant = np.clip(
    np.round(ps_cont * 100000) / 100000,
    0.5,
    2.5
)
```

TDS values remain continuous in the supplied version.

### Metadata correction required

In the final `Experiment_Info` table, the supplied source code currently records:

```python
str((0.1, 5))
```

for the PS bounds. This does not match the actual optimization bounds of `(0.5, 2.5)`.

Before publishing the code, replace it with:

```python
str((0.5, 2.5))
```

so that the Excel metadata agrees with the implemented search space.

---

## 4. Relay operating characteristics

Let:

\[
M=\frac{I}{I_{\mathrm{pickup}}}.
\]

The general IEC inverse-time expression is:

\[
t=TDS\frac{A}{M^B-1}.
\]

### 4.1 NI case

For the Normal Inverse characteristic:

\[
A=0.14,\qquad B=0.02.
\]

Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (0.14 / (ratio**0.02 - 1))
```

Recommended output prefix:

```python
excel_filename_prefix = (
    "COCSOS_15bus_TOF_TDS_newPS_NI_seed_protocol"
)
```

---

### 4.2 VI case

For the Very Inverse characteristic:

\[
A=13.5,\qquad B=1.
\]

Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (13.5 / (ratio - 1))
```

Recommended output prefix:

```python
excel_filename_prefix = (
    "COCSOS_15bus_TOF_TDS_newPS_VI_seed_protocol"
)
```

---

### 4.3 EI case

For the Extremely Inverse characteristic:

\[
A=80,\qquad B=2.
\]

The uploaded source file already uses:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (80 / (ratio**2 - 1))
```

Recommended output prefix:

```python
excel_filename_prefix = (
    "COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol"
)
```

---

### 4.4 Adaptive case

The Adaptive case should use the adaptive characteristic formulation defined in the manuscript and its dedicated source file.

A common adaptive representation is:

\[
t_i=TDS_i\frac{A}{M_i^B-1},
\]

where \(A\) and \(B\) are optimized rather than fixed.

Under a shared-\(A,B\) implementation, the organism may be encoded as:

\[
\mathbf{x}=
[TDS_1,\ldots,TDS_D,
PS_1,\ldots,PS_D,
A,B],
\]

giving:

\[
2D+2=86
\]

decision variables for \(D=42\).

The exact bounds, quantization steps, and interpretation of \(A\) and \(B\) must match the Adaptive code and the manuscript. They must not be inferred only by changing the EI constants.

Recommended output prefix:

```python
excel_filename_prefix = (
    "COCSOS_15bus_TOF_TDS_newPS_Adaptive_seed_protocol"
)
```

The Adaptive Excel output should additionally record:

- optimized \(A\);
- optimized \(B\);
- bounds of \(A\) and \(B\);
- quantization steps of \(A\) and \(B\);
- operating-time equation used for all relays.

---

### 4.5 Hybrid case

The Hybrid case should use the hybrid characteristic-selection mechanism defined in the manuscript and its dedicated source file.

A typical per-relay encoding is:

\[
\mathbf{x}=
[TDS_1,\ldots,TDS_D,
PS_1,\ldots,PS_D,
C_1,\ldots,C_D],
\]

where \(C_i\) identifies the characteristic assigned to relay \(i\), for example:

| Encoded value | Characteristic |
|---:|---|
| 1 | NI |
| 2 | VI |
| 3 | EI |

This gives:

\[
3D=126
\]

decision variables for \(D=42\).

The exact encoding and decoding rule must follow the Hybrid implementation. The characteristic variables must be discretized before objective evaluation.

Recommended output prefix:

```python
excel_filename_prefix = (
    "COCSOS_15bus_TOF_TDS_newPS_Hybrid_seed_protocol"
)
```

The Hybrid Excel output should additionally include:

- selected curve for every relay;
- encoded curve value;
- number of NI, VI, and EI relays;
- operating-time constants \(A_i\) and \(B_i\);
- characteristic-decoding rule.

> The supplied EI source file contains only `2D` variables and does not implement Adaptive or Hybrid encoding. Separate validated code versions are required for those two cases.

---

## 5. Objective function

The objective function minimizes the total primary-relay operating time plus constraint penalties:

\[
F(\mathbf{x})=
\sum_{i=1}^{D}t_i+
P_{\mathrm{primary}}+
P_{\mathrm{CTI}}.
\]

### Total primary operating time

```python
primary_obj = sum(primary_times)
```

### Minimum primary operating-time penalty

The code requires:

\[
t_i\geq0.015\ \mathrm{s}
\]

and applies:

\[
P_{\mathrm{primary}}
=
56000\sum_i
\max(0,0.015-t_i)^2.
\]

### Primary–backup coordination penalty

For each primary–backup pair:

\[
t_{\mathrm{backup}}-t_{\mathrm{primary}}
\geq CTI
\]

with:

\[
CTI=0.2\ \mathrm{s}.
\]

The penalty is:

\[
P_{\mathrm{CTI}}
=
500\sum_k
\max\left(
0,\,
CTI-
[t_{\mathrm{backup},k}-t_{\mathrm{primary},k}]
\right)^2.
\]

The reported `Best Fitness` is therefore the penalized objective, not necessarily the unpenalized sum of primary operating times.

---

## 6. COCSOS algorithm

The implementation contains the three original SOS phases:

1. Mutualism
2. Commensalism
3. Parasitism

It also incorporates:

### Comprehensive Opposition

The `co_population()` function generates candidates using:

- REO — Reflected Extended Opposition;
- QR — Quasi-Reflection;
- QO — Quasi-Opposition;
- EO — Extended Opposition.

The strategy probabilities vary with the iteration ratio.

The CO phase is applied with probability:

```python
0.4
```

per iteration.

### Chaotic Local Search

The `chaotic_local_search()` function uses a logistic map and population-difference perturbation around the best solution.

The default limit is:

```python
local_search_limit = 20
```

When CLS finds a better solution, the source code inserts that solution into the population at the pre-CLS best index and updates its fitness.

---

## 7. Recommended repository structure

Use one clearly named source file for each characteristic case:

```text
COCSOS-Problem3-Relay-Coordination/
│
├── README.md
├── requirements.txt
├── LICENSE
├── CITATION.cff
│
├── src/
│   ├── COCSOS_Problem3_NI.py
│   ├── COCSOS_Problem3_VI.py
│   ├── COCSOS_Problem3_EI.py
│   ├── COCSOS_Problem3_Adaptive.py
│   └── COCSOS_Problem3_Hybrid.py
│
├── seeds/
│   └── Problem3_Run_Seeds.xlsx
│
├── results/
│   ├── NI/
│   ├── VI/
│   ├── EI/
│   ├── Adaptive/
│   └── Hybrid/
│
└── docs/
    ├── relay_data_dictionary.md
    ├── characteristic_definitions.md
    └── experiment_protocol.md
```

A shared implementation may instead use one program and a command-line `--case` option, but the characteristic-selection logic must be explicitly implemented and tested.

---

## 8. Software requirements

Recommended environment:

- Python 3.9 or later
- NumPy
- Pandas
- OpenPyXL

Install the dependencies with:

```bash
pip install numpy pandas openpyxl
```

Suggested `requirements.txt`:

```text
numpy
pandas
openpyxl
```

---

## 9. Quick validation run

Before starting the official experiment, reduce:

```python
pop_size = 10
max_iter = 20
num_runs = 1
```

Then run one case and verify that:

- the program starts without an error;
- the 42-relay data load correctly;
- all 82 backup pairs are evaluated;
- the initial population is exported;
- convergence history has iterations 0 through 20;
- relay details are exported;
- backup coordination status is exported;
- both the per-run file and all-summary file are created.

Restore the official settings after the test.

---

## 10. Running the five cases

### 10.1 Windows Command Prompt

```bat
python src\COCSOS_Problem3_NI.py
python src\COCSOS_Problem3_VI.py
python src\COCSOS_Problem3_EI.py
python src\COCSOS_Problem3_Adaptive.py
python src\COCSOS_Problem3_Hybrid.py
```

### 10.2 Windows PowerShell

```powershell
python .\src\COCSOS_Problem3_NI.py
python .\src\COCSOS_Problem3_VI.py
python .\src\COCSOS_Problem3_EI.py
python .\src\COCSOS_Problem3_Adaptive.py
python .\src\COCSOS_Problem3_Hybrid.py
```

### 10.3 Linux or macOS

```bash
python3 src/COCSOS_Problem3_NI.py
python3 src/COCSOS_Problem3_VI.py
python3 src/COCSOS_Problem3_EI.py
python3 src/COCSOS_Problem3_Adaptive.py
python3 src/COCSOS_Problem3_Hybrid.py
```

Run the cases sequentially unless system resources and random-seed handling have been validated for parallel execution.

---

## 11. Recommended run order

Use the following order:

```text
NI → VI → EI → Adaptive → Hybrid
```

This order makes the output easier to review and follows the progression from fixed standard characteristics to more flexible characteristic models.

The order itself does not change the optimization result when every case uses a correctly assigned seed table and separate output filenames.

---

## 12. Seed protocol across the five cases

The source code assigns one seed to each independent run:

```text
Run 1  → Seed 1
Run 2  → Seed 2
...
Run 30 → Seed 30
```

Before population initialization, it resets:

```python
np.random.seed(seed)
random.seed(seed)
```

### Recommended fair-comparison protocol

Generate the run-seed table once and reuse it for all five cases:

```text
Problem3_Run_Seeds.xlsx
```

Do not independently regenerate seeds inside every characteristic file.

### Fixed NI, VI, and EI cases

These three cases have the same `2D=84` dimension and the same TDS/PS bounds.

When they use:

- the same run seed;
- the same population size;
- the same initialization order;
- the same quantization rule;
- no random call before initialization;

their initial TDS/PS populations can be identical.

### Adaptive and Hybrid cases

Adaptive and Hybrid may have different dimensions:

```text
Adaptive: commonly 2D + 2
Hybrid: commonly 3D
```

Using the same run seed still controls random variation, but the complete organisms cannot be identical because the search spaces differ.

For these cases:

- preserve identical initial TDS and PS components where the implementation permits;
- separately initialize the additional variables;
- document the initialization rule;
- compare results statistically over the same run count;
- do not claim that the full populations are identical when the dimensions differ.

### Master seed

The supplied source code uses:

```python
master_seed = None
```

Therefore, every complete execution creates a new seed table.

For publication-level reproducibility, either:

1. publish and reuse the generated `Run_Seeds` sheet; or
2. set a fixed master seed, for example:

```python
master_seed = 2026
```

---

## 13. Current official run settings

The supplied main block uses:

```python
bounds = (0.1, 1.1)
pop_size = 50
max_iter = 5000
total_dim = 2 * D
num_runs = 30
master_seed = None
```

The comment beside `num_runs` mentions 50 official runs, but the actual value is 30:

```python
num_runs = 30
```

The README and manuscript must report the executed value, not the outdated comment.

For 50 runs, change:

```python
num_runs = 50
```

and regenerate or supply a 50-row seed table.

---

## 14. Per-run output files

Each case generates one workbook per run.

Example for EI:

```text
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_1.xlsx
...
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_30.xlsx
```

Each workbook contains:

### `Summary`

- algorithm;
- problem;
- run;
- seed;
- dimension;
- relay count;
- population size;
- maximum iterations;
- initial best index;
- initial best objective value;
- initial best organism;
- elapsed time;
- final best fitness;
- final best solution.

### `Seed_Protocol`

- run seed;
- seed source;
- random libraries reset;
- reproducibility condition.

### `Experiment_Info`

- algorithm settings;
- TDS and PS bounds;
- relay count;
- total dimension;
- seed protocol;
- initial-population information.

### `Initial_Random_Pop`

Stores the complete population before the first CO transformation:

- run;
- seed;
- individual number;
- initial objective value;
- every decision variable.

For the fixed cases, the columns are:

```text
x1 ... x42   → TDS variables
x43 ... x84 → PS variables
```

Adaptive and Hybrid README sections or data dictionaries should document their additional columns.

### `Fitness History`

Stores:

- iteration 0: best objective value of the original random population;
- iterations 1 to 5000: best value after each COCSOS iteration;
- elapsed time.

### `Relay Details`

Stores:

- relay number;
- optimized TDS;
- optimized PS;
- pickup current;
- primary operating time.

Adaptive output should also include \(A\) and \(B\), where applicable.

Hybrid output should include the selected characteristic for every relay.

### `Backup Coordination`

Stores:

- primary relay;
- backup relay;
- primary operating time;
- backup operating time;
- coordination margin;
- required CTI;
- success or failure status.

---

## 15. Combined summary workbook

Each case creates one combined workbook.

Example:

```text
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_ALL_SUMMARY.xlsx
```

It contains:

- `All_Summary`;
- `Run_Seeds`;
- `Seed_Protocol`;
- `Experiment_Info`.

Use separate summary filenames for NI, VI, EI, Adaptive, and Hybrid to prevent overwriting.

---

## 16. Suggested output names

```text
NI/
COCSOS_15bus_TOF_TDS_newPS_NI_seed_protocol_ALL_SUMMARY.xlsx

VI/
COCSOS_15bus_TOF_TDS_newPS_VI_seed_protocol_ALL_SUMMARY.xlsx

EI/
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_ALL_SUMMARY.xlsx

Adaptive/
COCSOS_15bus_TOF_TDS_newPS_Adaptive_seed_protocol_ALL_SUMMARY.xlsx

Hybrid/
COCSOS_15bus_TOF_TDS_newPS_Hybrid_seed_protocol_ALL_SUMMARY.xlsx
```

Do not reuse the EI prefix for another characteristic.

---

## 17. Comparing the five cases

Recommended statistics include:

- best fitness;
- mean fitness;
- median fitness;
- standard deviation;
- worst fitness;
- total primary operating time without penalties;
- number of CTI violations;
- minimum coordination margin;
- mean coordination margin;
- runtime;
- convergence behavior;
- characteristic distribution for Hybrid;
- optimized \(A,B\) values for Adaptive.

### Feasibility check

A solution should not be considered fully feasible only because its penalized fitness is low.

Verify:

```text
Status = Success
```

for every row in `Backup Coordination`.

Also verify that every primary operating time satisfies:

\[
t_i\geq0.015\ \mathrm{s}.
\]

### Fairness statement

When comparing the five cases, report:

- identical relay data;
- identical CTI;
- identical penalty weights;
- identical run count;
- identical population size;
- identical iteration or evaluation budget;
- same seed table;
- differences in search-space dimension;
- additional variables used by Adaptive and Hybrid.

---

## 18. Input data included in the code

The source file embeds:

- 42 primary fault currents in `I_data`;
- backup fault currents in `I_data_backup`;
- 82 primary–backup pairs in `backup_pairs`;
- 42 CT ratios in `CT`;
- coordination interval `CTI = 0.2`.

For publication, also provide a separate machine-readable input file, for example:

```text
data/
├── relay_primary_currents.xlsx
├── relay_backup_currents.xlsx
├── primary_backup_pairs.xlsx
└── ct_ratios.xlsx
```

This allows readers to verify the embedded arrays independently.

---

## 19. Direct use of the optimizer

The fixed-characteristic optimizer can be called directly:

```python
best_solution, best_fitness, elapsed_time, history, initial_info = COCSOS(
    obj_func=objective_function,
    bounds=(0.1, 1.1),
    dim=2 * D,
    pop_size=50,
    max_iter=5000,
    seed=123456789,
    run=1
)
```

Returned values:

| Output | Description |
|---|---|
| `best_solution` | Final decision vector |
| `best_fitness` | Final penalized objective value |
| `elapsed_time` | Runtime in seconds |
| `history` | Best-fitness history |
| `initial_info` | Initial population, initial fitness values, seed, and initial best organism |

---

## 20. Numerical checks

### Operating-current ratio

The inverse-time equations require:

\[
M=\frac{I}{I_{\mathrm{pickup}}}>1.
\]

Before publishing results, verify that all primary and backup evaluations use valid ratios. If \(M\leq1\), the denominator can become zero or negative, producing invalid operating times.

A defensive implementation may use:

```python
def time_operation(TDS, Ipickup, I, A, B):
    ratio = I / Ipickup
    if ratio <= 1.0:
        return np.inf
    return TDS * (A / (ratio**B - 1.0))
```

Any such change must be applied consistently to every case and documented.

### Penalty versus reported operating time

The `Best Fitness` includes penalties. For tables in the paper, separately calculate and report:

```text
Raw total primary operating time
Penalty value
Penalized objective value
```

This avoids describing a penalized value as only the total operating time.

---

## 21. Troubleshooting

### Excel file is not created

Install the Excel engine:

```bash
pip install openpyxl
```

Close any workbook with the same filename before running the script.

### Results are different after rerunning the program

This is expected when:

```python
master_seed = None
```

Reuse the published `Run_Seeds` sheet or set a fixed master seed.

### NI, VI, and EI initial populations are different

Check that:

- all cases read the same seed table;
- no case generates a new table;
- all cases use dimension 84;
- all cases use identical bounds;
- no random call occurs before population generation;
- all cases use the same PS quantization method.

### Adaptive or Hybrid population does not match fixed cases

This is expected when the number of variables differs. Compare the shared TDS/PS components and document initialization of additional variables.

### Division by zero or negative operating time

Check whether:

```text
I / Ipickup <= 1
```

for any primary or backup operation.

### Output metadata reports incorrect PS bounds

Replace `(0.1, 5)` with `(0.5, 2.5)` in the final `Experiment_Info` table.

### The program says 30 runs although the comment says 50

The executed setting is determined by:

```python
num_runs = 30
```

Change it explicitly to 50 when required.

---

## 22. Recommended publication package

```text
Problem3-Reproducibility-Package/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
│
├── src/
│   ├── COCSOS_Problem3_NI.py
│   ├── COCSOS_Problem3_VI.py
│   ├── COCSOS_Problem3_EI.py
│   ├── COCSOS_Problem3_Adaptive.py
│   └── COCSOS_Problem3_Hybrid.py
│
├── data/
│   ├── relay_data.xlsx
│   └── data_dictionary.xlsx
│
├── seeds/
│   └── Problem3_Run_Seeds.xlsx
│
├── results/
│   ├── NI/
│   ├── VI/
│   ├── EI/
│   ├── Adaptive/
│   └── Hybrid/
│
└── analysis/
    ├── aggregate_results.py
    ├── statistical_tests.py
    └── generate_figures.py
```

---

## 23. Citation

When using this code or dataset, cite the associated paper:

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

Software citation template:

```bibtex
@software{Dang_COCSOS_Problem3,
  author  = {Dang, Tuan Khanh and Huynh, Nhat Huy and Truong, Khoa Hoang and Vo, Dieu Ngoc},
  title   = {COCSOS source code for directional overcurrent relay coordination under NI, VI, EI, Adaptive, and Hybrid characteristics},
  year    = {[Year]},
  version = {1.0.0},
  doi     = {[Software DOI]}
}
```

---

## 24. License

Add a license before publishing the repository.

Possible choices:

- MIT License;
- BSD 3-Clause License;
- GNU GPL-3.0.

The data license may be stated separately, for example:

```text
CC BY 4.0
```

---

## 25. Contact

For questions regarding the source code, experiment protocol, or reproduction of the relay-coordination results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---

## 26. Final checklist

Before uploading this problem to GitHub:

- [ ] Confirm the official number of runs: 30 or 50.
- [ ] Correct the PS metadata to `(0.5, 2.5)`.
- [ ] Assign unique filenames to all five cases.
- [ ] Reuse one `Run_Seeds` table.
- [ ] Verify NI, VI, and EI equations.
- [ ] Document Adaptive \(A,B\) encoding and bounds.
- [ ] Document Hybrid curve encoding and decoding.
- [ ] Save curve information in Adaptive and Hybrid Excel outputs.
- [ ] Check all 82 coordination pairs.
- [ ] Confirm all operating-current ratios are greater than one.
- [ ] Separate raw operating time from penalty values.
- [ ] Include complete initial populations.
- [ ] Include runtime and environment information.
- [ ] Add `requirements.txt`, `LICENSE`, and `CITATION.cff`.
- [ ] Archive the paper version of the repository with a DOI.