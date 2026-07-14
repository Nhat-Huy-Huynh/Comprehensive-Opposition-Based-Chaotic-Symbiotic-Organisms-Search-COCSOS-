# Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#requirements)
[![Reproducibility](https://img.shields.io/badge/reproducibility-code%20%2B%20data-brightgreen.svg)](#reproducibility-and-research-data)

## Authors

- **Tuan Khanh Dang**<sup>1,2</sup>
- **Nhat Huy Huynh**<sup>1,2</sup>
- **Khoa Hoang Truong**<sup>1,2</sup>
- **Dieu Ngoc Vo**<sup>1,2,*</sup>

<sup>1</sup> *[Affiliation 1 — to be completed]*  
<sup>2</sup> *[Affiliation 2 — to be completed]*  
<sup>*</sup> Corresponding author: *[email address — to be completed]*

---

## Overview

This repository contains the source code, test-system data, experiment configurations, random-seed protocol, and numerical results associated with the paper:

> **Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant**

The study proposes a new variant of the **Symbiotic Organisms Search (SOS)** algorithm for solving the optimal coordination problem of **directional overcurrent relays (DOCRs)** in distribution networks with distributed generation (DG).

The optimization framework aims to obtain reliable relay settings while minimizing relay operating times and satisfying all protection-coordination constraints.


---

## Optimization Problem

The relay-coordination problem is formulated as a constrained nonlinear optimization problem.

### Objective

The general objective is to minimize the total operating time of the primary relays:

$$
\min F(\mathbf{x})=\sum_{i=1}^{N_r} t_i
$$

where:

- $N_r$ is the number of relays;
- $t_i$ is the operating time of relay $i$;
- $\mathbf{x}$ is the vector of relay settings.

Depending on the investigated case, the objective function may also include penalty terms associated with coordination violations and other protection requirements.

### Primary–backup coordination constraint

For each primary–backup relay pair:

$$
t_{\mathrm{backup}}-t_{\mathrm{primary}}\geq \mathrm{CTI}
$$

where $\mathrm{CTI}$ is the required coordination time interval.

### Typical decision-variable constraints

$$
TDS_i^{\min}\leq TDS_i\leq TDS_i^{\max}
$$

$$
PS_i^{\min}\leq PS_i\leq PS_i^{\max}
$$

Additional relay-curve parameters may be optimized depending on the selected relay model.

--- 

## Requirements

Recommended environment:

- Python 3.10 or later
- NumPy
- Pandas
- SciPy
- OpenPyXL
- Matplotlib
- PyYAML
- Jupyter, optional
---

## Citation

When using this code or dataset, please cite the associated paper:

```bibtex
@article{Dang2026EfficientDOCR,
  title   = {Efficient Directional Overcurrent Relay Coordination in DG-Integrated Distribution Networks Using a New Symbiotic Organisms Search Variant},
  author  = {Dang, Tuan Khanh and Huynh, Nhat Huy and Truong, Khoa Hoang and Vo, Dieu Ngoc},
  journal = {Applied Soft Computing},
  year    = {2026},
  volume  = {[To be completed]},
  number  = {[To be completed]},
  pages   = {[To be completed]},
  doi     = {[To be completed]}
}
```
---

## Contact

For questions regarding the paper, code, or dataset, please contact:

**Prof. Dieu Ngoc Vo**  
Corresponding author  
Email: *[To be completed]*

For technical questions regarding code execution and result reproduction:

**Nhat Huy Huynh**  
Email: *[To be completed]*

---
