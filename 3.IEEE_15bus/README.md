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
| Independent runs in the supplied code | 50 |
| CO application probability | 0.4 |
| CLS trial limit | 20 |

---

## 3. Decision-variable bounds

The bounds actually used by the optimizer are:

| Variable | Lower bound | Upper bound |
|---|---:|---:|
| TDS | 0.1 | 1.1 |
| PS | 0.5 | 2.5 |

---

## 4. Relay operating characteristics
### 4.1 NI case

Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (0.14 / (ratio**0.02 - 1))
```
---

### 4.2 VI case
Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (13.5 / (ratio - 1))
```
---

### 4.3 EI case

The uploaded source file already uses:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (80 / (ratio**2 - 1))
```
---

### 4.4 Adaptive case

The Adaptive case should use the adaptive characteristic formulation defined in the manuscript and its dedicated source file.

The Adaptive Excel output should additionally record:

- optimized \(A\);
- optimized \(B\);
- bounds of \(A\) and \(B\);
- quantization steps of \(A\) and \(B\);
- operating-time equation used for all relays.

---

### 4.5 Hybrid case

The Hybrid case should use the hybrid characteristic-selection mechanism defined in the manuscript and its dedicated source file.

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

## 8. Software requirements

Recommended environment:

- Python 3.9 or later
- NumPy
- Pandas
- OpenPyXL

Install the dependencies with:

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
num_runs = 50
master_seed = None
```
---

## 14. Per-run output files

Each case generates one workbook per run.

Example for EI:

```text
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_1.xlsx
...
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_30.xlsx
```

---

## 18. Input data included in the code

The source file embeds:

- 42 primary fault currents in `I_data`;
- backup fault currents in `I_data_backup`;
- 82 primary–backup pairs in `backup_pairs`;
- 42 CT ratios in `CT`;
- coordination interval `CTI = 0.2`.
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
## 25. Contact

For questions regarding the source code, experiment protocol, or reproduction of the relay-coordination results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---