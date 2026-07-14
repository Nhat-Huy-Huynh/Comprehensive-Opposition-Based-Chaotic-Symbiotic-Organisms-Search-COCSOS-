# COCSOS_Original

## COCSOS for Directional Overcurrent Relay Coordination — Problem 3

This repository contains the **COCSOS** implementation used for **Problem 3: directional overcurrent relay coordination in a 42-relay distribution network**.

The study evaluates five relay-characteristic cases:

1. **NI** — Normal Inverse  
2. **VI** — Very Inverse  
3. **EI** — Extremely Inverse  
4. **Adaptive** — Optimized/adaptive inverse-time characteristic  
5. **Hybrid** — Mixed characteristic assignment among relays  

The code is associated with the paper:

> **Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant**

---

## 1. Authors

- Tuan Khanh Dang
- Nhat Huy Huynh
- Khoa Hoang Truong
- Dieu Ngoc Vo — Corresponding author

---

## 2. Problem Description

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

For the fixed-characteristic cases, namely NI, VI, and EI, each candidate solution contains:

$$
2D = 2 \times 42 = 84
$$

decision variables, including:

- $D=42$ Time Dial Setting variables;
- $D=42$ Plug Setting variables.

---

## 3. Decision-Variable Bounds

The bounds used by the optimizer are:

| Variable | Lower bound | Upper bound |
|---|---:|---:|
| TDS | 0.1 | 1.1 |
| PS | 0.5 | 2.5 |

The pickup current of relay $i$ is calculated from its Plug Setting and CT ratio:

$$
I_{\mathrm{pickup},i}=PS_i \times CT_i
$$

The TDS and PS values must remain within their corresponding limits throughout the optimization process.

> **Implementation note:** If the optimizer is called with a single common argument such as `bounds=(0.1, 1.1)`, the PS range of 0.5–2.5 must be handled through the solution-decoding, scaling, or objective-evaluation procedure implemented in the source code.

---

## 4. Relay Operating Characteristics

The general inverse-time relay operating-time equation is:

$$
t_i
=
TDS_i
\frac{A_i}
{\left(\frac{I_i}{I_{\mathrm{pickup},i}}\right)^{B_i}-1}
$$

where:

- $t_i$ is the relay operating time;
- $TDS_i$ is the Time Dial Setting;
- $I_i$ is the fault current observed by relay $i$;
- $I_{\mathrm{pickup},i}$ is the pickup current;
- $A_i$ and $B_i$ are the relay-characteristic constants.

### 4.1. NI Case

For the Normal Inverse characteristic:

$$
A=0.14,\qquad B=0.02
$$

The corresponding operating-time equation is:

$$
t
=
TDS
\frac{0.14}
{\left(\frac{I}{I_{\mathrm{pickup}}}\right)^{0.02}-1}
$$

Python implementation:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (0.14 / (ratio**0.02 - 1))
```

---

### 4.2. VI Case

For the Very Inverse characteristic:

$$
A=13.5,\qquad B=1
$$

The corresponding operating-time equation is:

$$
t
=
TDS
\frac{13.5}
{\left(\frac{I}{I_{\mathrm{pickup}}}\right)-1}
$$

Python implementation:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (13.5 / (ratio - 1))
```

---

### 4.3. EI Case

For the Extremely Inverse characteristic:

$$
A=80,\qquad B=2
$$

The corresponding operating-time equation is:

$$
t
=
TDS
\frac{80}
{\left(\frac{I}{I_{\mathrm{pickup}}}\right)^2-1}
$$

Python implementation:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (80 / (ratio**2 - 1))
```

---

### 4.4. Adaptive Case

The Adaptive case must use the adaptive characteristic formulation defined in the manuscript and its dedicated source file.

The relay operating time is calculated as:

$$
t_i
=
TDS_i
\frac{A_i}
{\left(\frac{I_i}{I_{\mathrm{pickup},i}}\right)^{B_i}-1}
$$

In this case, $A_i$ and $B_i$ are optimized together with the relay settings.

The Adaptive Excel output should additionally record:

- optimized $A_i$ values;
- optimized $B_i$ values;
- lower and upper bounds of $A$;
- lower and upper bounds of $B$;
- quantization steps of $A$ and $B$;
- operating-time equation used for all relays.

The exact number and arrangement of decision variables must follow the validated Adaptive implementation.

---

### 4.5. Hybrid Case

The Hybrid case must use the hybrid characteristic-selection mechanism defined in the manuscript and its dedicated source file.

The characteristic assigned to each relay is represented by an encoded variable:

| Encoded value | Characteristic |
|---:|---|
| 1 | NI |
| 2 | VI |
| 3 | EI |

For $D=42$, the Hybrid candidate solution contains:

$$
3D=3\times42=126
$$

decision variables, consisting of:

- 42 TDS variables;
- 42 PS variables;
- 42 characteristic-selection variables.

The exact encoding and decoding rules must follow the validated Hybrid implementation. The characteristic-selection variables must be discretized before objective-function evaluation.

A typical decoding instruction is:

```python
curve_code = np.clip(
    np.rint(curve_variable),
    1,
    3
).astype(int)
```

The decoding rule is:

```text
1 → NI
2 → VI
3 → EI
```

The characteristic constants are assigned as follows:

| Characteristic | A | B |
|---|---:|---:|
| NI | 0.14 | 0.02 |
| VI | 13.5 | 1.00 |
| EI | 80.0 | 2.00 |

Recommended output prefix:

```python
excel_filename_prefix = (
    "COCSOS_15bus_TOF_TDS_newPS_Hybrid_seed_protocol"
)
```

The Hybrid Excel output should additionally include:

- selected characteristic for every relay;
- encoded characteristic value;
- number of NI relays;
- number of VI relays;
- number of EI relays;
- operating-time constants $A_i$ and $B_i$;
- characteristic-encoding and decoding rules.

> **Important:** The supplied EI source file contains only $2D$ variables and does not implement Adaptive or Hybrid encoding. Separate validated code versions are required for these two cases.

---

## 5. Objective Function

The objective function minimizes the total primary-relay operating time together with constraint penalties:

$$
F(\mathbf{x})
=
\sum_{i=1}^{D}t_i
+
P_{\mathrm{primary}}
+
P_{\mathrm{CTI}}
$$

The reported `Best Fitness` is therefore the penalized objective-function value, not necessarily the unpenalized sum of primary-relay operating times.

### 5.1. Total Primary-Relay Operating Time

The main objective component is:

$$
F_{\mathrm{primary}}
=
\sum_{i=1}^{D}t_i
$$

Python implementation:

```python
primary_obj = sum(primary_times)
```

---

### 5.2. Minimum Primary Operating-Time Constraint

Each primary relay must satisfy:

$$
t_i\geq0.015\ \mathrm{s}
$$

A violation occurs when:

$$
t_i<0.015\ \mathrm{s}
$$

The corresponding penalty is:

$$
P_{\mathrm{primary}}
=
56000
\sum_{i=1}^{D}
\left[
\max\left(0,\ 0.015-t_i\right)
\right]^2
$$

Python implementation:

```python
primary_penalty = 56000 * sum(
    max(0.0, 0.015 - t_i) ** 2
    for t_i in primary_times
)
```

---

### 5.3. Primary–Backup Coordination Constraint

For every primary–backup relay pair $k$, the following constraint must be satisfied:

$$
t_{\mathrm{backup},k}
-
t_{\mathrm{primary},k}
\geq CTI
$$

The coordination time interval is:

$$
CTI=0.2\ \mathrm{s}
$$

The coordination violation of pair $k$ is:

$$
v_k
=
\max
\left(
0,\ 
CTI-
\left[
t_{\mathrm{backup},k}
-
t_{\mathrm{primary},k}
\right]
\right)
$$

The coordination penalty is:

$$
P_{\mathrm{CTI}}
=
500
\sum_{k=1}^{82}
v_k^2
$$

Equivalently:

$$
P_{\mathrm{CTI}}
=
500
\sum_{k=1}^{82}
\left[
\max
\left(
0,\ 
CTI-
\left[
t_{\mathrm{backup},k}
-
t_{\mathrm{primary},k}
\right]
\right)
\right]^2
$$

Python implementation:

```python
cti_penalty = 500 * sum(
    max(
        0.0,
        CTI - (t_backup - t_primary)
    ) ** 2
    for t_primary, t_backup in coordination_times
)
```

---

### 5.4. Final Penalized Objective

The final fitness value is calculated as:

$$
F
=
F_{\mathrm{primary}}
+
P_{\mathrm{primary}}
+
P_{\mathrm{CTI}}
$$

Python implementation:

```python
fitness = primary_obj + primary_penalty + cti_penalty
```

A solution with a small total primary operating time may still have a large fitness value if it violates the minimum-time or coordination constraints.

---

## 6. COCSOS Parameters

The principal COCSOS settings used in the supplied code are:

| Parameter | Value |
|---|---:|
| Population size | 50 |
| Maximum iterations | 5000 |
| Independent runs | 50 |
| CO application probability | 0.4 |
| CLS trial limit | 20 |
| Coordination interval | 0.2 s |

The COCSOS implementation includes:

- the original SOS interaction phases;
- the Competitive Opposition mechanism;
- the Chaotic Local Search mechanism;
- best-solution tracking;
- convergence-history recording;
- seeded population initialization;
- Excel result export.

---

## 7. Software Requirements

Recommended environment:

- Python 3.9 or later;
- NumPy;
- Pandas;
- OpenPyXL.

---

## 8. Installation

Install the required dependencies with:

```bash
pip install numpy pandas openpyxl
```

To verify the Python version:

```bash
python --version
```

To verify the installed packages:

```bash
pip show numpy pandas openpyxl
```

---

## 9. Running the Code

Place the selected Python source file in the working directory and run:

```bash
python your_script_name.py
```

For example:

```bash
python COCSOS_Problem3_EI.py
```

Each characteristic case should use:

- its own validated source file;
- its own output filename prefix;
- the appropriate objective-function implementation;
- the same published or reused seed table when conducting a fair comparison.

---

## 10. Recommended Run Order

Use the following order:

```text
NI → VI → EI → Adaptive → Hybrid
```

This order follows the progression from fixed standard characteristics to more flexible characteristic models.

The order does not affect the optimization results when:

- each case uses the correctly assigned seed table;
- random generators are reset before initialization;
- output filenames are separated;
- no result file from one case overwrites another case.

---

## 11. Seed Protocol Across the Five Cases

The source code assigns one seed to each independent run:

```text
Run 1  → Seed for Run 1
Run 2  → Seed for Run 2
...
Run 50 → Seed for Run 50
```

Before population initialization, both random-number generators are reset:

```python
np.random.seed(seed)
random.seed(seed)
```

This ensures that the population generated for a run can be reproduced when the same seed, dimensionality, population size, variable bounds, and initialization procedure are used.

### 11.1. Master Seed

The supplied source code uses:

```python
master_seed = None
```

Therefore, each complete program execution generates a new seed table.

For publication-level reproducibility, use one of the following approaches.

#### Option 1: Publish and reuse the generated seed table

Save the generated seeds in the `Run_Seeds` worksheet and use the same seed table for all five cases.

#### Option 2: Use a fixed master seed

For example:

```python
master_seed = 2026
```

The fixed master seed allows the run-seed table to be regenerated deterministically.

---

### 11.2. Fair Comparison Between Cases

For a controlled comparison among NI, VI, EI, Adaptive, and Hybrid, the seed assigned to each run should be kept the same:

```text
NI Run 1       → Seed S1
VI Run 1       → Seed S1
EI Run 1       → Seed S1
Adaptive Run 1 → Seed S1
Hybrid Run 1   → Seed S1
```

The same rule should be applied from Run 1 to Run 50.

However, using the same seed does not always produce numerically identical initial populations when the cases have different dimensions. For example:

- NI, VI, and EI use $2D=84$ variables;
- Hybrid uses $3D=126$ variables;
- Adaptive may use another dimension depending on its encoding.

The common seed still provides a controlled random-number stream, but only cases with identical dimensions, bounds, and initialization procedures can produce identical initial population matrices.

---

## 12. Current Official Run Settings

The supplied main block uses:

```python
bounds = (0.1, 1.1)
pop_size = 50
max_iter = 5000
total_dim = 2 * D
num_runs = 50
master_seed = None
```

For the fixed NI, VI, and EI cases:

```python
total_dim = 2 * D
```

With $D=42$:

```python
total_dim = 84
```

For the Hybrid case:

```python
total_dim = 3 * D
```

With $D=42$:

```python
total_dim = 126
```

The Adaptive dimension must follow the validated Adaptive source code.

> **Note:** The argument `bounds=(0.1, 1.1)` may represent normalized or general optimizer bounds in the supplied implementation. The actual TDS and PS limits must still be handled according to the variable-group mapping implemented in the objective function or solution-decoding function.

---

## 13. Per-Run Output Files

Each case generates one workbook for every independent run.

Example for the EI case:

```text
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_1.xlsx
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_2.xlsx
...
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol_run_50.xlsx
```

Separate filename prefixes should be used for each case:

```text
COCSOS_15bus_TOF_TDS_newPS_NI_seed_protocol
COCSOS_15bus_TOF_TDS_newPS_VI_seed_protocol
COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol
COCSOS_15bus_TOF_TDS_newPS_Adaptive_seed_protocol
COCSOS_15bus_TOF_TDS_newPS_Hybrid_seed_protocol
```

This prevents workbooks from different characteristic cases from overwriting one another.

---

## 14. Recommended Excel Output

Depending on the supplied source-code version, each run workbook should record at least:

- run number;
- seed;
- best fitness;
- total primary operating time;
- primary operating-time penalty;
- CTI coordination penalty;
- optimized TDS values;
- optimized PS values;
- pickup currents;
- primary operating times;
- backup operating times;
- primary–backup coordination margins;
- CTI violations;
- convergence history;
- elapsed time;
- initial population;
- initial objective-function values.

For the Adaptive case, the workbook should additionally record:

- optimized $A_i$ values;
- optimized $B_i$ values;
- $A$ and $B$ bounds;
- quantization steps;
- adaptive operating-time equations.

For the Hybrid case, the workbook should additionally record:

- encoded characteristic value for each relay;
- decoded characteristic name;
- number of NI relays;
- number of VI relays;
- number of EI relays;
- assigned $A_i$ values;
- assigned $B_i$ values;
- characteristic-decoding rule.

---

## 15. Input Data Included in the Code

The source file embeds:

- 42 primary fault currents in `I_data`;
- backup fault currents in `I_data_backup`;
- 82 primary–backup pairs in `backup_pairs`;
- 42 CT ratios in `CT`;
- coordination interval `CTI = 0.2`.

The relay data must remain aligned by index. For relay $i$:

```text
TDS[i]
PS[i]
CT[i]
I_data[i]
```

must refer to the same relay.

Similarly, every entry in `backup_pairs` must use the same relay-index convention as the current and decision-variable arrays.

---

## 16. Direct Use of the Optimizer

The fixed-characteristic optimizer can be called directly as follows:

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

The principal returned values are:

| Returned value | Description |
|---|---|
| `best_solution` | Best candidate solution found |
| `best_fitness` | Best penalized objective-function value |
| `elapsed_time` | Execution time of the run |
| `history` | Best-fitness convergence history |
| `initial_info` | Initial population and initial objective information |

For the Hybrid implementation, the dimension must be changed to:

```python
dim = 3 * D
```

The direct function call must also use the Hybrid-specific objective and decoding functions.

---

## 17. Interpreting the Results

The `Best Fitness` value is the penalized objective:

$$
F
=
\sum_{i=1}^{D}t_i
+
P_{\mathrm{primary}}
+
P_{\mathrm{CTI}}
$$

Therefore:

$$
\text{Best Fitness}
\neq
\sum_{i=1}^{D}t_i
$$

whenever any constraint penalty is nonzero.

A feasible solution should satisfy:

$$
t_i\geq0.015\ \mathrm{s},
\qquad
\forall i
$$

and:

$$
t_{\mathrm{backup},k}
-
t_{\mathrm{primary},k}
\geq0.2\ \mathrm{s},
\qquad
\forall k
$$

For a feasible solution:

$$
P_{\mathrm{primary}}=0
$$

and:

$$
P_{\mathrm{CTI}}=0
$$

Consequently:

$$
F
=
\sum_{i=1}^{D}t_i
$$

When reviewing the output, both the best fitness and the unpenalized total operating time should be reported.

---

## 18. Reproducibility Checklist

Before publishing or comparing results, verify that:

1. The same run-seed table is used across all compared cases.
2. Both `numpy.random` and Python `random` are reset before initialization.
3. NI, VI, and EI use the correct $A$ and $B$ constants.
4. Adaptive uses its validated $A$- and $B$-optimization mechanism.
5. Hybrid discretizes characteristic variables before objective evaluation.
6. TDS and PS values remain within their prescribed bounds.
7. The number of primary–backup pairs is 82.
8. The coordination interval is 0.2 s.
9. Each case has a separate output filename prefix.
10. The generated seed table is saved with the experimental results.
11. The initial population and initial objective-function values are retained.
12. The best fitness is distinguished from the unpenalized total operating time.

---

## 19. Citation

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

Replace the placeholder publication information after the final bibliographic data become available.

---

## 20. Contact

For questions regarding the source code, experimental protocol, or reproduction of the relay-coordination results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---