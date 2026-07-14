# Comprehensive-Opposition-Based-Chaotic-Symbiotic-Organisms-Search-COCSOS-
COCSOS algorithm
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

## Research Motivation

The integration of distributed generation changes fault-current magnitude and direction in distribution networks. These changes can cause:

- loss of relay selectivity;
- relay miscoordination;
- increased relay operating time;
- violation of the coordination time interval;
- incorrect primary–backup relay operation;
- difficulty in selecting suitable pickup-current and time-dial settings.

The proposed SOS variant is developed to improve the search process and obtain high-quality relay settings for DG-integrated distribution systems.

---

## Main Contributions

1. A new SOS-based optimization variant for efficient DOCR coordination.
2. A relay-coordination model suitable for DG-integrated distribution networks.
3. Simultaneous optimization of relay decision variables, such as time dial setting, pickup-current setting, and relay characteristic parameters where applicable.
4. Explicit treatment of primary–backup relay coordination constraints.
5. A reproducible experiment protocol based on predefined random seeds.
6. Comprehensive comparisons with the original SOS algorithm and other benchmark optimizers.
7. Detailed export of relay settings, operating times, coordination margins, convergence histories, and runtime results.

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

## Proposed Algorithm

The proposed method is a new variant of the **Symbiotic Organisms Search** algorithm.

The original SOS framework models interactions among organisms in an ecosystem through three main phases:

1. **Mutualism phase**
2. **Commensalism phase**
3. **Parasitism phase**

The proposed variant introduces additional search mechanisms to improve the balance between exploration and exploitation, accelerate convergence, and reduce the probability of premature convergence.

> **Algorithm acronym:** *[Insert the official acronym used in the manuscript, e.g., COCSOS]*

A detailed description, mathematical formulation, and pseudocode are provided in the associated paper.

---

## Repository Structure

```text
repository/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── environment.yml
│
├── src/
│   ├── proposed_sos.py
│   ├── original_sos.py
│   ├── objective_function.py
│   ├── relay_operating_time.py
│   ├── constraint_handling.py
│   ├── seed_protocol.py
│   └── export_results.py
│
├── data/
│   ├── test_system_01/
│   ├── test_system_02/
│   ├── relay_data.xlsx
│   ├── fault_current_data.xlsx
│   └── primary_backup_pairs.xlsx
│
├── config/
│   ├── algorithm_parameters.yaml
│   ├── experiment_settings.yaml
│   └── run_function_seeds.xlsx
│
├── experiments/
│   ├── run_single_case.py
│   ├── run_all_cases.py
│   ├── run_original_sos.py
│   └── run_proposed_sos.py
│
├── results/
│   ├── proposed_algorithm/
│   ├── original_sos/
│   ├── comparison_algorithms/
│   ├── convergence_history/
│   └── statistical_analysis/
│
├── notebooks/
│   ├── result_analysis.ipynb
│   └── figure_generation.ipynb
│
└── docs/
    ├── data_dictionary.md
    ├── experiment_protocol.md
    └── test_system_description.md
```

The actual directory names may differ slightly from this template.

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

Install the required packages with:

```bash
pip install -r requirements.txt
```

For full environment reproduction:

```bash
conda env create -f environment.yml
conda activate docr-sos
```

---

## How to Run

### 1. Run a single test case

```bash
python experiments/run_single_case.py \
    --algorithm proposed \
    --case test_system_01 \
    --run 1
```

### 2. Run the original SOS algorithm

```bash
python experiments/run_original_sos.py \
    --case test_system_01
```

### 3. Run the proposed SOS variant

```bash
python experiments/run_proposed_sos.py \
    --case test_system_01
```

### 4. Run all experiments

```bash
python experiments/run_all_cases.py
```

### 5. Generate summary files

```bash
python src/export_results.py
```

The generated files are stored in the `results/` directory.

> Update the commands above to match the final filenames and command-line arguments used in the public repository.

---

## Input Data

The test-system data may include:

- relay identifiers;
- primary and backup relay pairs;
- primary fault currents;
- backup fault currents;
- current-transformer ratios;
- pickup-current limits;
- time-dial limits;
- relay characteristic parameters;
- coordination time interval;
- distributed-generation operating scenarios;
- near-end and far-end fault conditions;
- thermal or protection constraints, where applicable.

The meaning, unit, and format of each input field should be described in:

```text
docs/data_dictionary.md
```

---

## Output Data

The program exports numerical results in Excel or CSV format, including:

- best objective value;
- optimized relay settings;
- primary relay operating times;
- backup relay operating times;
- coordination time intervals;
- constraint violations;
- primary–backup pair details;
- convergence history;
- random seeds;
- initial population information;
- runtime;
- statistical summaries.

Typical Excel sheets include:

```text
SUMMARY
TDS & OPERATING TIME
BACKUP PAIRS DETAILS
CONVERGENCE HISTORY
RUN-FUNCTION SEEDS
EXPERIMENT INFO
RUNTIME
```

---

## Reproducibility and Research Data

To ensure a fair and reproducible comparison:

- each independent run uses a predefined random seed;
- the proposed algorithm and comparison algorithms use the same seed protocol;
- the initial population is generated before the optimization process begins;
- seed information is stored for every run and test case;
- initial and final objective values are recorded;
- complete numerical results are provided in the associated data repository.

The experiment package should include:

```text
run_function_seeds.xlsx
initial_populations/
initial_objective_values/
complete_run_results/
convergence_history/
statistical_results/
```

### Research data repository

Complete Excel result files and supporting data are available at:

> **Dataset DOI:** *[Insert Zenodo or Mendeley Data DOI]*

### Source-code archive

The archived version of the source code used for the paper is available at:

> **Software DOI:** *[Insert Zenodo DOI for the GitHub release]*

The latest development version is maintained in this GitHub repository.

---

## Experimental Settings

The main experiment settings should be reported in `config/experiment_settings.yaml`, including:

```yaml
independent_runs: 50
population_size: 50
maximum_iterations: 1000
initialization: uniform
seed_policy: one_seed_per_run_and_case
boundary_handling: clipping
coordination_time_interval: 0.2
execution_mode: sequential
```

Replace the example values with the exact settings used in the paper.

Algorithm-specific parameters should be provided in:

```text
config/algorithm_parameters.yaml
```

---

## Statistical Analysis

The repository may include scripts for calculating:

- best value;
- mean value;
- median;
- standard deviation;
- worst value;
- success rate;
- Wilcoxon signed-rank test;
- Friedman ranking;
- win/tie/loss comparison;
- average runtime.

Run the analysis with:

```bash
python analysis/statistical_analysis.py
```

---

## Figures and Tables

Scripts used to reproduce the figures and tables in the paper should be included whenever possible.

Examples:

```bash
python analysis/generate_tables.py
python analysis/generate_figures.py
```

The scripts should generate:

- convergence curves;
- relay operating-time plots;
- coordination-margin plots;
- statistical comparison tables;
- runtime comparisons;
- optimized relay-setting tables.

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

For the software archive:

```bibtex
@software{Dang2026DOCRCode,
  author  = {Dang, Tuan Khanh and Huynh, Nhat Huy and Truong, Khoa Hoang and Vo, Dieu Ngoc},
  title   = {Source code for efficient directional overcurrent relay coordination using a new SOS variant},
  year    = {2026},
  version = {1.0.0},
  doi     = {[Software DOI]}
}
```

For the research dataset:

```bibtex
@dataset{Dang2026DOCRData,
  author    = {Dang, Tuan Khanh and Huynh, Nhat Huy and Truong, Khoa Hoang and Vo, Dieu Ngoc},
  title     = {Experimental data for efficient directional overcurrent relay coordination in DG-integrated distribution networks},
  year      = {2026},
  version   = {1},
  publisher = {[Zenodo or Mendeley Data]},
  doi       = {[Dataset DOI]}
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

## Acknowledgments

The authors acknowledge the support of:

> *[Funding agency, project number, laboratory, institution, or research group — to be completed]*

---

## Disclaimer

This repository is provided for academic research and reproducibility purposes. The authors are not responsible for protection-system settings applied directly to real power systems without independent engineering verification, relay-manufacturer validation, and compliance with applicable protection standards.
