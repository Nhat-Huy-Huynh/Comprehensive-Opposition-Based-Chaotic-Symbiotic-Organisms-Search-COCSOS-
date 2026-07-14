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

## 1. Authors

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

TDS bounds are set in the main block:

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

### 4.1 NI case

Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    ratio = min(ratio, 20.0)
    return TDS * (0.14 / (ratio**0.02 - 1.0))
```
---

### 4.2 VI case

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    ratio = min(ratio, 20.0)
    return TDS * (13.5 / (ratio - 1.0))
```
---

### 4.3 EI case
Use:

```python
def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    ratio = min(ratio, 20.0)
    return TDS * (80.0 / (ratio**2 - 1.0))
```
---

### 4.4 Adaptive case

The Adaptive case optimizes inverse-time characteristic parameters in addition to TDS and PS.

The dedicated Adaptive implementation must explicitly define:

- lower and upper bounds of \(A\);
- lower and upper bounds of \(B\);
- quantization steps of \(A\) and \(B\);
- whether \(A,B\) are shared or relay-specific;
- initialization order;
- Excel output columns for \(A,B\).
---

### 4.5 Hybrid case

The Hybrid case permits each relay to use NI, VI, or EI.

A possible mapping is:

| Encoded value | Characteristic | \(A\) | \(B\) |
|---:|---|---:|---:|
| 1 | NI | 0.14 | 0.02 |
| 2 | VI | 13.5 | 1 |
| 3 | EI | 80 | 2 |

---
## 5. Software requirements

Recommended environment:

- Python 3.9 or later
- NumPy
- Pandas
- OpenPyXL

---

## 6. Default execution settings

The uploaded VI source file currently uses:

```python
bounds = (0.05, 3)
pop_size = 100
max_iter = 5000
total_dim = 2 * D
num_runs = 20
function_name = "COCSOS_VI_110kV"
```

---

## 7. Random-seed protocol

The program assigns one seed to each `Run–Function` pair.

Before initialization, it resets:

```python
np.random.seed(seed)
random.seed(seed)
```
The seed table is saved so that SOS or another comparison algorithm can reuse the same seeds.

---

## 8. Direct use of the optimizer

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
---

## 9. Citation

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

## 10. Contact

For questions regarding the code, experimental protocol, or reproduction of the 90-relay results, contact:

- **Nhat Huy Huynh** — *[email to be added]*
- **Dieu Ngoc Vo** — Corresponding author, *[email to be added]*
---