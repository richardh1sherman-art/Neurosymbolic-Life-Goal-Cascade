# Neurosymbolic Life-Goal Cascade & Multi-Timescale Inverter-Dominated Grid Control

**Author:** Richard Sherman (Member, IEEE — System Architecture Invariant Manifest Group, Keller, TX)  
**Target Hardware:** NVIDIA DGX Spark (Grace Blackwell ARM64 / CUDA 13.0) & Julia EMT Simulation Environment

---

## 1. Research Portfolio & Publication Index

This repository houses the complete mathematical specifications, LaTeX manuscripts, electromagnetic transient (EMT) testbeds, and multi-agent control scripts spanning four interconnected research papers:

| Paper | Title | Submission Venues | Core Source / Manuscript |
| :--- | :--- | :--- | :--- |
| **Paper 1** | *Decentralized Cyber-Physical Stabilization of Coupled Kuramoto Oscillators via Emergent MARL CSMA/CD Protocols* | arXiv (`submit/8296238`) | `infer_story_logic.py`, `social_gnn_mesh.py` |
| **Paper 2** | *Symmetric Self-Adaptive Contraction Manifold for Wide-Area Inverter Control Under Severe Multiplicative Phase Noise* | *IEEE Trans. Smart Grid* & arXiv (`submit/8362651`) | `Documents/area_control_revision.tex` (`Documents/area_control_revision.pdf`) |
| **Paper 3** | *Tie-Line Scheduling Using Real-Time Contraction Metrics: Hierarchical Reachable Sets for Multi-Area Inverter-Dominated Grids* | *IEEE Trans. Power Systems* & [arXiv:2611.21858](https://arxiv.org) ([DOI](https://doi.org)) | `Documents/tie_line_sccm_paper.tex` (`Documents/tie_line_sccm_paper.pdf`) |
| **Paper 4** | *Scale-Invariant Contraction Hierarchies: Group-Theoretic Cohesion, Coupling Augmentation, and Compactness Propagation* | Working Draft (`Documents/scale_invariant_hierarchy.pdf`) | `Documents/scale_invariant_hierarchy.tex`, `verify_scale_invariant_hierarchy.py` |

---

## 2. Three-Tier Control Architecture Overview

To stabilize **100% inverter-based resource (IBR)** transmission networks with **zero synchronous generators (0 SGs)**, this codebase unifies online parameter estimation with nested Riemannian contraction manifolds across three timescales:

1. **Device Layer (< 1 ms — Sub-Millisecond Inverter Protection):**
   * Enforces transistor overcurrent limits (`I_max <= 1.20 p.u.`) and Phase-Locked Loop (PLL) synchronization margins via local contraction multipliers (`alpha_i`).
   * Driven by live bi-level Prediction Error Method and Moving Horizon Estimation (**PEM-MHE**) parameter tracking without requiring a prior plant model.
2. **Area Layer (ms — Intra-Area Cohesion & Mode-Shift Healing):**
   * Separates voltage-forming **state-space cohesion (`C`)** from **PLL synchronization coupling (`P`)** across heterogeneous Grid-Forming (GFM) and Grid-Following (GFL) devices.
   * Uses **hierarchical shallow decision trees** parameterized by live PEM-MHE estimates to detect GFM-to-GFL current-limit fallback within **52.0 ms** and engage chatter-free Schmitt-trigger hysteresis damping.
3. **Grid Layer (1 s — Distributed Nonlinear SCCM & Supervisory Interface):**
   * Replaces convex online ADMM consensus with a **Distributed Nonlinear Separable Control Contraction Metric (SCCM)** executing closed-form straight-line geodesic feedback (`u_i* + K_i(theta_hat_i)(x_i - x_i*)`) over single-hop neighbor state broadcasts.
   * Computes **Pontryagin attainable (reachable) ellipsoids** (`R_Grid <= R_Area <= R_Dev`) certified via Schur-complement inclusion LMIs, and projects `R_Grid` through network Power Transfer Distribution Factors (PTDFs) to export safe thermal reserves to slow supervisory optimizers.

---

## 3. Repository Code & Experiment Map

### A. Core Area Contraction & Coupling Analysis (Paper 2 & Paper 3)
* **`compute_coupling_matrices.py`**: Extracts the `10 x 10` Kron-reduced susceptance network to construct the **State-Space Cohesion (`C`)** and **PLL Synchronization Coupling (`P`)** matrices across GFM, GFL, and SG units.
* **`coupled_LMI_solver.py`**: Solves the 20-state sparse off-diagonal Control Contraction Metric LMI (`Psi_11 <= 0`), tightening worst-case tie-line L2 disturbance gain from `gamma_diag* = 0.4162 p.u.` to `gamma_coupled* = 0.4015 p.u.` (**+3.65%** margin gain).
* **`area_mpc_optimizer.py` & `plot_mpc_contraction.py`**: Implements the Certainty-Equivalent Adaptive MPC outer manifold (**+82.35%** contraction margin expansion under `3.0 deg -> 15.0 deg` multiplicative phase noise).
* **`run_ieee39_transients.jl` & `audit_grid_waveforms.py`**: Julia `PowerSimulationsDynamics.jl` EMT simulation and Python waveform audit pipeline for the modified IEEE 39-bus testbed.

### B. Online Mode-Shift Detection, Hysteresis & 100%-IBR Stress Tests
* **`detect_gfm_to_gfl_shift.py`**: Online Zhou–Köhler PEM-MHE estimator detecting GFM current-rail saturation and fallback into GFL mode within **52.0 ms**.
* **`heal_gfm_to_gfl_shift.py` & `heal_multi_device_hysteresis.py`**: Schmitt-trigger hysteresis controller (`60 ms` dwell) stabilizing simultaneous `GFM-31` mode drift and `GFL-30` `15.0 deg` tie-line jitter with **zero chattering** (`lambda_max <= -1.0594`).
* **`test_100pct_ibr_area.py`**: Verifies full 100% IBR operation (**0 SGs, 7 GFMs, 3 GFLs**), achieving `gamma_100ibr* = 0.4018 p.u.` (within **0.06%** of the legacy SG baseline) and maintaining `lambda_max <= -2.4312` under simultaneous faults.
* **`test_gfm_reduction_threshold.py`**: Sweeps GFM anchor share from 7 GFMs down to 1 GFM, proving that reducing `N_GFM` from `6 -> 3` avoids blackout (`I_max = 1.0429 p.u. <= 1.20 p.u.`) and survives down to `1 GFM / 9 GFL` (`1.1480 p.u.`).

### C. IEEE 118-Bus 3-Area Reachable Sets, MARL & Lossy Links (Paper 3)
* **`three_area_sccm_reachability.py`**:
  * Synthesizes closed-form geodesic SCCM gains across Device (`lambda = 4.50`), Area (`lambda = 2.40`), and Grid (`lambda = 1.25`) layers.
  * Computes Pontryagin reachable ellipsoids in `(V_pu, I_pu)` space (`I_max = 1.0431 p.u.`).
  * Verifies Schur-complement tube containment (`lambda_min = +1041.08` for `R_Grid <= R_Area`, `+225.26` for `R_Area <= R_Dev`).
  * Exports certified PTDF thermal reserve (**13.46 MW** reserve / **586.54 MW** safe dispatch ceiling on bottleneck Line 59) directly into the 3-area IEEE 118-bus supervisory coordinator (`comm-limited-congestion-mgmt-main/`).
* **`three_area_multitimescale_bridge.py` & `compare_mit_baseline.py`**: Benchmarks the 3-tier stack against the non-communicating supervisory baseline during a `+140 MW` Area 1 surge + parallel Line 66 trip, cutting cumulative tie-line overload from **230.8 MW·s** (101.3% peak) to **39.7 MW·s** (**-82.8%**).
* **`marl_three_area_emergency.py` & `inspect_prop_delay.py`**: Evaluates isolated decentralized area agents under realistic 1-hop (`1 s`) and 2-hop (`2 s`) shadow-price propagation delays (**142.8 MW·s** overload, **-38.1%**).
* **`test_packet_loss_resilience.py`**: Tests Zero-Order Hold (ZOH) + decay buffering under **25% random packet loss** and a **3 s total link blackout**, holding cumulative overload to **192.5 MW·s** while keeping `lambda_max <= -2.7300`.

---


### D. Caltech 28-Bus Digital Twin, MIT OSQP-Julia EMT Co-Simulation & Hybrid Automaton (Paper 3 & Paper 4)
* **`test_caltech_device_pem_mhe.py` & `caltech_mit_unified_demo.py`**: Anti-aliased 40 ms integral PEM-MHE tracker under Caltech 0.625 deg^2 sync noise linked to the IEEE 118-bus coordinator (`Documents/caltech_mit_emt_comparison.pdf`, `Documents/TopologyCaltech.pdf`).
* **`mit_sccm_closed_loop_eval.py`, `run_true_mit_qp_rollout.py` & `run_true_mit_emt_closed_loop.py` + `emt_mit_step_worker.jl`**: Closed-loop Python sparse OSQP + Julia `PowerSimulationsDynamics.jl` (`Rodas5P`) co-simulation.
* **`BridgeObserver.py`, `CoTangent_Lifting.py`, `events_hybrid_reachability.py` & `run_steps123_hybrid_bifurcation.py`**: Cotangent-lifted self-similar wreath recursion, 14-bit Caltech switching words, and Hopf bifurcation verification.

## 4. Quickstart Execution (DGX Spark ARM64 Environment)

Activate the CUDA-enabled Python environment (`smt-ilp-env`) and run the end-to-end verification suite:

```bash
source /home/rsherman/projects/SMT-ILP/smt-ilp-env/bin/activate
cd /home/rsherman/projects/SMT-ILP/ZeroVRAM

# 1. Verify 100% IBR (0 SG) Area Stability & Hysteresis Healing
python3 test_100pct_ibr_area.py
python3 test_gfm_reduction_threshold.py

# 2. Verify 3-Tier Pontryagin Reachable Sets, Schur Containment & IEEE 118-Bus PTDF Export
python3 three_area_sccm_reachability.py

# 3. Verify 3-Area Multi-Timescale Surge Relief & Packet-Loss Resilience
python3 compare_mit_baseline.py
python3 test_packet_loss_resilience.py
```

---

## 5. Key References
* H. S. Shiromoto, M. Revay, and I. R. Manchester, *"Distributed nonlinear control design using separable control contraction metrics,"* arXiv:1810.04794v1, 2018.
* G. J. Pappas, G. Lafferriere, and S. Sastry, *"Hierarchically consistent control systems,"* in *Proc. 37th IEEE CDC*, 1998, pp. 4336–4341.
* J. Y. Chen *et al.*, *"Communication-limited multi-agent grid congestion management via differentiable optimization,"* in *Proc. ACM e-Energy '26*, 2026, pp. 486–503.
* Y. Zhou and J. Köhler, *"Scalable identification of physics-based and neural dynamics from partial measurements,"* arXiv:2412.01997, 2024.
* J. D. Lara *et al.*, *"Revisiting power systems time-domain simulation methods and models,"* *IEEE Trans. Power Syst.*, vol. 39, no. 2, pp. 2421–2437, Mar. 2024.
