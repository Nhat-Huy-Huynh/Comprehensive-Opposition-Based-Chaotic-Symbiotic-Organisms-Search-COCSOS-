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

---

## 4. Relay Operating Characteristics

### 4.1. NI Case

For the Normal Inverse characteristic:

$$
A=0.14,\qquad B=0.02
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

Python implementation:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (80 / (ratio**2 - 1))
```

---

### 4.4. Adaptive Case

The Adaptive case must use the adaptive characteristic formulation defined in the manuscript and its dedicated source file.

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

---
## 5. COCSOS Parameters

The principal COCSOS settings used in the supplied code are:

| Parameter | Value |
|---|---:|
| Population size | 50 |
| Maximum iterations | 5000 |
| Independent runs | 50 |
| CO application probability | 0.4 |
| CLS trial limit | 20 |
| Coordination interval | 0.2 s |

---

## 6. Software Requirements

Recommended environment:

- Python 3.9 or later;
- NumPy;
- Pandas;
- OpenPyXL.

---

## 7. Seed Protocol Across the Five Cases

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
The seed table is saved so that SOS or another comparison algorithm can reuse the same seeds.

This ensures that the population generated for a run can be reproduced when the same seed, dimensionality, population size, variable bounds, and initialization procedure are used.

## 8. Current Official Run Settings

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

## 9. Per-Run Output Files

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

## 10. Input Data Included in the Code

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

## 11. Direct Use of the Optimizer

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
---

## 12. Citation

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

## 13. Contact

For questions regarding the source code, experimental protocol, or reproduction of the relay-coordination results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*

---