# COCSOS for 90-Relay Directional Overcurrent Relay Coordination — Problem 4

This repository contains the **COCSOS** implementation used for **Problem 4: optimal coordination of 90 directional overcurrent relays** in a high-voltage distribution or sub-transmission network.

The study evaluates five relay-characteristic cases:

1. **NI** — Normal Inverse
2. **VI** — Very Inverse
3. **EI** — Extremely Inverse
4. **Adaptive** — optimized inverse-time characteristic parameters
5. **Hybrid** — relay-by-relay selection among NI, VI, and EI characteristics

The code is associated with the paper:

> **Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant**

## Authors

- Tuan Khanh Dang
- Nhat Huy Huynh
- Khoa Hoang Truong
- Dieu Ngoc Vo — Corresponding author

---

## 2. Problem data

The current implementation contains:

| Item | Value |
|---|---:|
| Number of relays | 90 |
| Number of primary–backup pairs | 188 |
| Current-transformer ratio | 1200 for every relay |
| Coordination time interval | 0.2 s |
| Near-fault current data | 90 values |
| Mid-fault current data | 90 values |
| Far-fault current data | 90 values |
| Relay probability/weight factors | 90 values |
| Fixed-characteristic decision variables | 180 |
| Population size | 100 |
| Maximum iterations | 5000 |
| Independent runs in the supplied code | 20 |
| CO application probability | 0.4 |
| Chaotic local-search trials | 20 |

---

## 3. Decision variables

### 3.1 Time Dial Setting

The TDS bounds are:

\[
0.05\leq TDS_i\leq3.
\]

These bounds are set in the main block:

```python
bounds = (0.05, 3)
```

### 3.2 Plug Setting

Each relay has its own PS lower and upper bounds. The complete 90-element bound vectors are embedded in the `COCSOS()` function.

```python
lb = [                      0.340, 0.340, 0.533, 0.533, 0.800, 0.800,
                            0.407, 0.407, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.407, 0.407, 0.407, 0.407,
                            0.800, 0.800, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.800, 0.100, 0.800, 0.800,
                            0.100, 0.800, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.800, 0.800, 0.340, 0.340,
                            0.533, 0.533, 0.340, 0.340, 0.533, 0.533,
                            0.340, 0.340, 0.340, 0.340, 0.340, 0.340,
                            0.340, 0.340, 0.340, 0.340, 0.533, 0.533,
                            0.340, 0.340, 0.407, 0.407, 0.533, 0.533,
                            0.533, 0.600, 0.533, 0.600, 0.533, 0.533,
                            0.340, 0.130, 0.340, 0.210, 0.533, 0.533,
                            0.340, 0.130, 0.407, 0.407, 0.407, 0.407]
ub = [                      0.850, 0.850, 1.333, 1.333, 2.000, 2.000,
                            1.017, 1.017, 2.000, 2.000, 2.000, 2.000,
                            2.000, 2.000, 2.000, 2.000, 2.000, 2.000,
                            2.000, 2.000, 1.017, 1.017, 1.017, 1.017,
                            2.000, 2.000, 2.000, 2.000, 2.000, 2.000,
                            1.400, 2.000, 2.000, 0.500, 2.000, 2.000,
                            0.500, 2.000, 2.000, 2.000, 2.000, 2.000,
                            2.000, 2.000, 2.000, 2.000, 0.850, 0.850,
                            1.333, 1.333, 0.850, 0.850, 1.333, 1.333,
                            0.850, 0.850, 0.850, 0.850, 0.850, 0.850,
                            0.850, 0.850, 0.850, 0.850, 1.333, 1.333,
                            0.850, 0.850, 1.017, 1.017, 1.333, 1.333,
                            1.333, 0.700, 1.333, 0.700, 1.333, 1.333,
                            0.850, 0.147, 0.850, 0.241, 1.333, 1.333,
                            0.850, 0.147, 1.017, 1.017, 1.017, 1.017 ]
```
---

## 4. Relay operating characteristics

Let:

\[
M=\frac{I}{I_{\mathrm{pickup}}}.
\]

The general IEC inverse-time equation is:

\[
t=TDS\frac{A}{M^B-1}.
\]

The supplied code also limits the current ratio to:

\[
M\leq20.
\]

### 4.1 NI case

For Normal Inverse:

\[
A=0.14,\qquad B=0.02.
\]

Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    ratio = min(ratio, 20.0)
    return TDS * (0.14 / (ratio**0.02 - 1.0))
```

Recommended identifiers:

```python
function_name = "COCSOS_NI_110kV"
output_prefix = "COCSOS_OF3_110kV_TDS_newPS_NI"
```

---

### 4.2 VI case

For Very Inverse:

\[
A=13.5,\qquad B=1.
\]

This is the characteristic already implemented in the uploaded file:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    ratio = min(ratio, 20.0)
    return TDS * (13.5 / (ratio - 1.0))
```

Recommended identifiers:

```python
function_name = "COCSOS_VI_110kV"
output_prefix = "COCSOS_OF3_110kV_TDS_newPS_VI"
```

---

### 4.3 EI case

For Extremely Inverse:

\[
A=80,\qquad B=2.
\]

Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    ratio = min(ratio, 20.0)
    return TDS * (80.0 / (ratio**2 - 1.0))
```

Recommended identifiers:

```python
function_name = "COCSOS_EI_110kV"
output_prefix = "COCSOS_OF3_110kV_TDS_newPS_EI"
```

---

### 4.4 Adaptive case

The Adaptive case optimizes inverse-time characteristic parameters in addition to TDS and PS.

A common shared-parameter encoding is:

\[
\mathbf{x}=
[TDS_1,\ldots,TDS_{90},
PS_1,\ldots,PS_{90},
A,B]
\]

with:

\[
\dim(\mathbf{x})=2D+2=182.
\]

The operating time becomes:

\[
t_i=TDS_i\frac{A}{M_i^B-1}.
\]

The dedicated Adaptive implementation must explicitly define:

- lower and upper bounds of \(A\);
- lower and upper bounds of \(B\);
- quantization steps of \(A\) and \(B\);
- whether \(A,B\) are shared or relay-specific;
- initialization order;
- Excel output columns for \(A,B\).

Recommended identifiers:

```python
function_name = "COCSOS_Adaptive_110kV"
output_prefix = "COCSOS_OF3_110kV_TDS_newPS_Adaptive"
```

Do not obtain the Adaptive case by only replacing the constants in the VI file. The solution encoding and bounds must also be updated.

---

### 4.5 Hybrid case

The Hybrid case permits each relay to use NI, VI, or EI.

A typical encoding is:

\[
\mathbf{x}=
[TDS_1,\ldots,TDS_{90},
PS_1,\ldots,PS_{90},
C_1,\ldots,C_{90}]
\]

where \(C_i\) is the characteristic assigned to relay \(i\).

A possible mapping is:

| Encoded value | Characteristic | \(A\) | \(B\) |
|---:|---|---:|---:|
| 1 | NI | 0.14 | 0.02 |
| 2 | VI | 13.5 | 1 |
| 3 | EI | 80 | 2 |

This gives:

\[
\dim(\mathbf{x})=3D=270.
\]

The dedicated Hybrid code must define:

- discrete encoding and decoding of \(C_i\);
- rounding or repair of characteristic variables;
- operating-time evaluation for each relay;
- characteristic information exported to Excel;
- counts of NI, VI, and EI relays in the final solution.

Recommended identifiers:

```python
function_name = "COCSOS_Hybrid_110kV"
output_prefix = "COCSOS_OF3_110kV_TDS_newPS_Hybrid"
```

The uploaded VI code has only 180 variables and does not implement the Hybrid characteristic block.

---

## 5. Objective function

The objective combines weighted operating times at three fault locations with constraint penalties.

For relay \(i\), the weighted operating-time term is:

\[
J_i=
p_i
\left(
0.2t_{i,\mathrm{near}}
+
0.6t_{i,\mathrm{mid}}
+
0.2t_{i,\mathrm{far}}
\right)
\]

where \(p_i\) is stored in `p_jump`.

The total raw objective is:

\[
J_{\mathrm{raw}}=
\sum_{i=1}^{90}J_i.
\]

The optimized objective is:

\[
F(\mathbf{x})=
J_{\mathrm{raw}}+
P_{\mathrm{primary}}+
P_{\mathrm{ratio}}+
P_{\mathrm{CTI}}.
\]

---

## 6. Constraint penalties

### 6.1 Minimum operating time

The code requires:

\[
t_{i,\mathrm{near}}\geq0.015\ \mathrm{s}.
\]

The penalty is:

\[
P_{\mathrm{primary}}
=
20000
\sum_i
\max(0,0.015-t_i)^2.
\]

### 6.2 Minimum current ratio

For every relay:

\[
\frac{I_{i,\mathrm{far}}}{I_{\mathrm{pickup},i}}\geq1.2.
\]

The penalty is:

\[
P_{\mathrm{ratio}}
=
1000
\sum_i
\max
\left(
0,
1.2-
\frac{I_{i,\mathrm{far}}}{I_{\mathrm{pickup},i}}
\right)^2.
\]

### 6.3 Primary–backup coordination

For each of the 188 primary–backup pairs:

\[
t_{\mathrm{backup}}-t_{\mathrm{primary}}
\geq0.2\ \mathrm{s}.
\]

The penalty is:

\[
P_{\mathrm{CTI}}
=
5000
\sum_k
\max
\left(
0,
0.2-
[t_{\mathrm{backup},k}-t_{\mathrm{primary},k}]
\right)^2.
\]

`Best Fitness` is therefore a penalized objective value and should not be described only as total operating time.

For publication, report separately:

- raw weighted operating-time objective;
- total penalty;
- final penalized fitness;
- number of violated constraints.

---

## 7. COCSOS algorithm

The implementation includes the original SOS phases:

1. Mutualism
2. Commensalism
3. Parasitism

It also includes:

### Comprehensive Opposition

`co_population()` generates alternative candidates using:

- REO — Reflected Extended Opposition;
- QR — Quasi-Reflection;
- QO — Quasi-Opposition;
- EO — Extended Opposition.

The selection probabilities change with the iteration ratio.

The CO phase is activated with probability:

```python
0.4
```

per iteration.

### Chaotic Local Search

`chaotic_local_search()` uses the logistic map:

\[
z_{k+1}=4z_k(1-z_k)
\]

and a population-difference perturbation around the current best solution.

The default local-search limit is:

```python
local_search_limit = 20
```

When CLS finds an improvement, the improved solution is inserted into the population and its fitness is updated.

---

## 8. Recommended repository structure

```text
COCSOS-Problem4-90Relay/
│
├── README.md
├── requirements.txt
├── LICENSE
├── CITATION.cff
│
├── src/
│   ├── COCSOS_90Relay_NI.py
│   ├── COCSOS_90Relay_VI.py
│   ├── COCSOS_90Relay_EI.py
│   ├── COCSOS_90Relay_Adaptive.py
│   └── COCSOS_90Relay_Hybrid.py
│
├── data/
│   ├── relay_currents.xlsx
│   ├── primary_backup_pairs.xlsx
│   ├── ps_bounds.xlsx
│   └── data_dictionary.xlsx
│
├── seeds/
│   └── Problem4_Run_Function_Seeds.xlsx
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

## 9. Software requirements

Recommended environment:

- Python 3.9 or later
- NumPy
- Pandas
- OpenPyXL

Install dependencies with:

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

## 10. Running a quick validation test

Before running the official experiment, change:

```python
pop_size = 10
max_iter = 20
num_runs = 1
```

Then verify that:

- the program loads all 90 relay records;
- all 188 primary–backup pairs are processed;
- no invalid current ratio occurs;
- the initial random and quantized populations are exported;
- the convergence history contains iterations 0–20;
- relay operating times are exported;
- the backup-coordination table is exported;
- the per-run and summary files are created.

After validation, restore the official settings.

---

## 11. Running the five cases

### Windows Command Prompt

```bat
python src\COCSOS_90Relay_NI.py
python src\COCSOS_90Relay_VI.py
python src\COCSOS_90Relay_EI.py
python src\COCSOS_90Relay_Adaptive.py
python src\COCSOS_90Relay_Hybrid.py
```

### Windows PowerShell

```powershell
python .\src\COCSOS_90Relay_NI.py
python .\src\COCSOS_90Relay_VI.py
python .\src\COCSOS_90Relay_EI.py
python .\src\COCSOS_90Relay_Adaptive.py
python .\src\COCSOS_90Relay_Hybrid.py
```

### Linux or macOS

```bash
python3 src/COCSOS_90Relay_NI.py
python3 src/COCSOS_90Relay_VI.py
python3 src/COCSOS_90Relay_EI.py
python3 src/COCSOS_90Relay_Adaptive.py
python3 src/COCSOS_90Relay_Hybrid.py
```

Recommended run order:

```text
NI → VI → EI → Adaptive → Hybrid
```

Use separate result directories and output prefixes for every case.

---

## 12. Default execution settings

The uploaded VI source file currently uses:

```python
bounds = (0.05, 3)
pop_size = 100
max_iter = 5000
total_dim = 2 * D
num_runs = 20
function_name = "COCSOS_VI_110kV"
```

The source-code comment refers to 30 runs, but the executed value is:

```python
num_runs = 20
```

The paper and README must report the actual executed value.

To run 30 independent trials:

```python
num_runs = 30
```

To run 50 independent trials:

```python
num_runs = 50
```

---

## 13. Random-seed protocol

The program assigns one seed to each `Run–Function` pair.

Before initialization, it resets:

```python
np.random.seed(seed)
random.seed(seed)
```

The seed table is saved so that SOS or another comparison algorithm can reuse the same seeds.

### Important limitation

The seed table is generated with:

```python
rng = np.random.default_rng()
```

without a fixed master seed.

Therefore:

- every complete rerun creates a different seed table;
- published experiments can only be reproduced if the saved seed table is retained;
- comparison algorithms must read the original table rather than regenerate seeds.

For full reproducibility, either:

1. publish the generated `Function_Seeds` sheet; or
2. modify the function to use a fixed master seed, for example:

```python
rng = np.random.default_rng(2026)
```

---

## 14. Seed use across NI, VI, EI, Adaptive, and Hybrid

### NI, VI, and EI

These cases share:

- 180 variables;
- identical TDS bounds;
- identical relay-specific PS bounds;
- identical population size;
- identical quantization logic.

They can therefore use the same complete initial population when:

- the same seed table is used;
- no random call occurs before initialization;
- the initialization order is identical.

### Adaptive

A shared-\(A,B\) Adaptive case commonly has 182 variables.

The complete population cannot be identical to the 180-variable cases. For a controlled comparison:

- initialize the common 180 TDS/PS variables first;
- preserve them across cases;
- then initialize \(A,B\);
- document the additional-variable initialization.

### Hybrid

A per-relay Hybrid case commonly has 270 variables.

The full population cannot be identical to NI, VI, or EI. Recommended practice:

- preserve the common TDS/PS blocks;
- initialize the curve-selection block separately;
- use the same run seed or a documented derived seed;
- do not claim identical full initial populations.

---

## 15. Initial-population recording

The program stores both:

1. `Initial Random Population`
2. `Initial Quantized Population`

The initial objective values are computed from the quantized population:

```python
fitness_random_initial = np.array([
    obj_func(ind)
    for ind in pop_random_initial_quantized
])
```

The Excel output therefore allows verification of:

- raw initial organisms;
- quantized initial organisms;
- objective value of every initial organism;
- initial best organism;
- initial best objective value.

Iteration 0 in the convergence history represents the best objective value of the initial quantized population before the first CO transformation.

---

## 16. Per-run Excel output

The uploaded code currently generates filenames such as:

```text
COCSOS_OF3_110kV_TDS_newPS_VI_1.xlsx.xlsx
```

The duplicate extension should be corrected to:

```python
filename = f"COCSOS_OF3_110kV_TDS_newPS_VI_{run}.xlsx"
```

Recommended filenames:

```text
COCSOS_OF3_110kV_TDS_newPS_NI_run_1.xlsx
COCSOS_OF3_110kV_TDS_newPS_VI_run_1.xlsx
COCSOS_OF3_110kV_TDS_newPS_EI_run_1.xlsx
COCSOS_OF3_110kV_TDS_newPS_Adaptive_run_1.xlsx
COCSOS_OF3_110kV_TDS_newPS_Hybrid_run_1.xlsx
```

Each workbook contains:

### `Summary`

- algorithm;
- run;
- function/case;
- seed;
- dimension;
- bounds;
- population size;
- maximum iterations;
- initial best index;
- initial best objective value;
- initial best organism;
- elapsed time;
- final best fitness;
- final best solution.

### `Seed_Protocol`

- run and function;
- seed;
- seed source;
- random libraries reset;
- reproducibility condition.

### `Experiment_Info`

- seed protocol;
- initial-population definition;
- meaning of iteration 0;
- requirements for reproducing the initialization.

### `Fitness History`

- iteration;
- best fitness;
- elapsed time.

### `Relay Details`

For each of the 90 relays:

- TDS;
- PS;
- pickup current;
- primary operating time for near fault;
- primary operating time for mid fault;
- primary operating time for far fault.

Adaptive output should also include \(A,B\).

Hybrid output should also include the selected characteristic and its \(A,B\) constants.

### `Backup Coordination`

For each of the 188 pairs:

- primary relay;
- backup relay;
- primary operating time;
- backup operating time;
- coordination margin;
- CTI;
- success/failure status.

### `Initial_Random_Pop_OF`

Contains the unquantized initial population.

### `Initial_Quantized_Pop_OF`

Contains the quantized initial population used for initial objective evaluation.

---

## 17. Combined summary workbook

The current VI code creates:

```text
COCSOS_OF3_110kV_TDS_newPS_VI_ALL_SUMMARY.xlsx
```

It contains:

- `All_Summary`;
- `Function_Seeds`;
- `Run_Function_Seeds`;
- `Experiment_Info`.

Recommended files for the five cases:

```text
COCSOS_OF3_110kV_TDS_newPS_NI_ALL_SUMMARY.xlsx
COCSOS_OF3_110kV_TDS_newPS_VI_ALL_SUMMARY.xlsx
COCSOS_OF3_110kV_TDS_newPS_EI_ALL_SUMMARY.xlsx
COCSOS_OF3_110kV_TDS_newPS_Adaptive_ALL_SUMMARY.xlsx
COCSOS_OF3_110kV_TDS_newPS_Hybrid_ALL_SUMMARY.xlsx
```

---

## 18. Direct use of the optimizer

For a fixed characteristic:

```python
best_solution, best_fitness, elapsed_time, history, initial_info = COCSOS(
    obj_func=objective_function,
    bounds=(0.05, 3),
    dim=2 * D,
    pop_size=100,
    max_iter=5000,
    seed=123456789
)
```

Returned values:

| Output | Description |
|---|---|
| `best_solution` | Final TDS and PS vector |
| `best_fitness` | Final penalized objective value |
| `elapsed_time` | Runtime in seconds |
| `history` | Best-fitness history |
| `initial_info` | Initial populations, initial fitness, seed, and initial best organism |

---

## 19. Comparing the five cases

Recommended metrics include:

- best fitness;
- mean fitness;
- median fitness;
- standard deviation;
- worst fitness;
- raw weighted operating-time objective;
- total penalty;
- number of CTI violations;
- minimum CTI margin;
- average CTI margin;
- number of far-current ratio violations;
- convergence behavior;
- runtime;
- optimized \(A,B\) for Adaptive;
- number of NI, VI, and EI relays for Hybrid.

### Feasibility requirements

A final solution should satisfy:

\[
t_{\mathrm{backup}}-t_{\mathrm{primary}}\geq0.2\ \mathrm{s}
\]

for every pair,

\[
t_{i,\mathrm{near}}\geq0.015\ \mathrm{s},
\]

and:

\[
\frac{I_{i,\mathrm{far}}}{I_{\mathrm{pickup},i}}\geq1.2.
\]

Do not determine feasibility only from a low penalized objective.

---

## 20. Important implementation checks

### 20.1 Current-ratio validation

The inverse-time formula requires:

\[
M>1.
\]

A defensive implementation is:

```python
def time_operation(TDS, Ipickup, I, A, B):
    ratio = I / Ipickup
    if ratio <= 1.0:
        return np.inf
    ratio = min(ratio, 20.0)
    return TDS * (A / (ratio**B - 1.0))
```

Apply the same rule consistently in all five cases.

### 20.2 CO quantization and fitness consistency

In the supplied code, the CO combined population is evaluated before the selected population is quantized:

```python
fitness_combined = np.array([
    obj_func(ind, iteration)
    for ind in combined
])

pop = combined[best_indices]
pop = np.array([
    quantize_solution(ind, lb, ub)
    for ind in pop
])

fitness = fitness_combined[best_indices]
```

If quantization changes a selected organism, its stored fitness may no longer correspond to the stored organism.

Before publishing results, use one consistent sequence:

```python
combined = np.array([
    quantize_solution(ind, lb, ub)
    for ind in combined
])

fitness_combined = np.array([
    obj_func(ind, iteration)
    for ind in combined
])
```

Then select the best organisms.

### 20.3 Runtime interpretation

`elapsed_time` is measured inside `COCSOS()` and excludes most Excel-writing time. State this in the paper and repository.

### 20.4 File extension

Correct `.xlsx.xlsx` to `.xlsx`.

### 20.5 Run count

The code executes 20 runs, despite comments referring to 30 runs.

---

## 21. Troubleshooting

### Excel file is not created

Install OpenPyXL:

```bash
pip install openpyxl
```

Close any workbook with the same filename.

### Results differ after rerunning the script

This is expected because the seed generator has no fixed master seed. Reuse the saved seed table or set a master seed.

### NI, VI, and EI initial populations differ

Verify:

- the same seed table is used;
- dimensions are all 180;
- TDS and PS bounds are identical;
- no random call occurs before `np.random.uniform`;
- quantization is identical.

### Adaptive or Hybrid populations differ

This is expected because their dimensions may be 182 and 270. Compare the shared TDS/PS blocks instead of the complete organism.

### Invalid or negative operating time

Check whether:

```text
I / Ipickup <= 1
```

for the evaluated relay and fault current.

### Fitness and solution appear inconsistent after CO

Quantize the combined population before objective evaluation or recompute fitness after quantization.

### Output file has two `.xlsx` extensions

Remove one extension in the filename template.

---


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


---


---

## 25. Contact

For questions regarding the code, experimental protocol, or reproduction of the 90-relay results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---

## 26. Final checklist

Before publishing Problem 4:

- [ ] Confirm the official run count: 20, 30, or 50.
- [ ] Correct the duplicate `.xlsx.xlsx` extension.
- [ ] Use separate filenames for all five cases.
- [ ] Reuse one published seed table.
- [ ] Verify NI, VI, and EI equations.
- [ ] Document Adaptive \(A,B\) bounds and encoding.
- [ ] Document Hybrid characteristic encoding.
- [ ] Export \(A,B\) for Adaptive.
- [ ] Export the selected curve for every Hybrid relay.
- [ ] Verify all 188 primary–backup pairs.
- [ ] Verify the minimum operating-time constraint.
- [ ] Verify the far-fault current-ratio constraint.
- [ ] Quantize CO candidates before evaluating fitness.
- [ ] Separate raw objective and penalty in reported results.
- [ ] Publish initial random and quantized populations.
- [ ] Report Python, NumPy, Pandas, CPU, RAM, and operating system.
- [ ] Add `requirements.txt`, `LICENSE`, and `CITATION.cff`.
- [ ] Archive the paper version of the repository with a DOI.