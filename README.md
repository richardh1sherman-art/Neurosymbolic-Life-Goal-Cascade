# Neurosymbolic Life-Goal Cascade & Multi-Timescale Inverter-Dominated Grid Control

**Author:** Richard Sherman (Member, IEEE — System Architecture Invariant Manifest Group, Keller, TX)  
**Target Hardware:** NVIDIA DGX Spark (Grace Blackwell ARM64 / CUDA 13.0) & Julia EMT Simulation Environment

---

## 1. Research Portfolio & Publication Index

This repository houses the complete mathematical specifications, LaTeX manuscripts, electromagnetic transient (EMT) testbeds, and multi-agent control scripts spanning three interconnected research papers:

| Paper | Title | Submission Venues | Core Source / Manuscript |
| :--- | :--- | :--- | :--- |
| **Paper 1** | *Decentralized Cyber-Physical Stabilization of Coupled Kuramoto Oscillators via Emergent MARL CSMA/CD Protocols* | arXiv (`submit/8296238`) | `infer_story_logic.py`, `social_gnn_mesh.py` |
| **Paper 2** | *Symmetric Self-Adaptive Contraction Manifold for Wide-Area Inverter Control Under Severe Multiplicative Phase Noise* | *IEEE Trans. Smart Grid* & arXiv (`submit/8362651`) | `area_control_revision.tex` (`area_control_revision.pdf`) |
| **Paper 3** | *Tie-Line Scheduling Using Real-Time Contraction Metrics: Hierarchical Reachable Sets for Multi-Area Inverter-Dominated Grids* | *IEEE Trans. Power Systems* & arXiv (`submit/8383032`) | `tie_line_sccm_paper.tex` (`tie_line_sccm_paper.pdf`) |

---

## 2. Three-Tier Control Architecture Overview

To stabilize $100\%$ inverter-based resource (IBR) transmission networks with **zero synchronous generators ($0\text{ SGs}$)**, this codebase unifies online parameter estimation with nested Riemannian contraction manifolds across three timescales:

1. **Device Layer ($<1\text{ ms}$ — Sub-Millisecond Inverter Protection):**
   * Enforces transistor overcurrent limits ($I_{\max} \le 1.20\text{ p.u.}$) and Phase-Locked Loop (PLL) synchronization margins via local contraction multipliers ($\alpha_i$).
   * Driven by live bi-level Prediction Error Method and Moving Horizon Estimation (**PEM-MHE**) parameter tracking without requiring a prior plant model.
2. **Area Layer ($\text{ms}$ — Intra-Area Cohesion & Mode-Shift Healing):**
   * Separates voltage-forming **state-space cohesion ($\mathbf{C}$)** from **PLL synchronization coupling ($\mathbf{P}$)** across heterogeneous Grid-Forming (GFM) and Grid-Following (GFL) devices.
   * Uses **hierarchical shallow decision trees** parameterized by live PEM-MHE estimates to detect GFM-to-GFL current-limit fallback within **$52.0\text{ ms}$** and engage chatter-free Schmitt-trigger hysteresis damping.
3. **Grid Layer ($1\text{ s}$ — Distributed Nonlinear SCCM & Supervisory Interface):**
   * Replaces convex online ADMM consensus with a **Distributed Nonlinear Separable Control Contraction Metric (SCCM)** executing closed-form straight-line geodesic feedback ($u_i^* + K_i(\hat{\theta}_i)(x_i - x_i^*)$) over single-hop neighbor state broadcasts.
   * Computes **Pontryagin attainable (reachable) ellipsoids** ($\mathcal{R}_{\text{Grid}} \subseteq \mathcal{R}_{\text{Area}} \subseteq \mathcal{R}_{\text{Dev}}$) certified via Schur-complement inclusion LMIs, and projects $\mathcal{R}_{\text{Grid}}^\infty$ through network Power Transfer Distribution Factors (PTDFs) to export safe thermal reserves to slow supervisory optimizers.

---

## 3. Repository Code & Experiment Map

### A. Core Area Contraction & Coupling Analysis (Paper 2 & Paper 3)
* **`compute_coupling_matrices.py`**: Extracts the $10 \times 10$ Kron-reduced susceptance network to construct the **State-Space Cohesion ($\mathbf{C}$)** and **PLL Synchronization Coupling ($\mathbf{P}$)** matrices across GFM, GFL, and SG units.
* **`coupled_LMI_solver.py`**: Solves the 20-state sparse off-diagonal Control Contraction Metric LMI ($\mathbf{\Psi}_{11} \preceq 0$), tightening worst-case tie-line $L_2$ disturbance gain from $\gamma_{\text{diag}}^* = 0.4162\text{ p.u.}$ to $\gamma_{\text{coupled}}^* = 0.4015\text{ p.u.}$ ($+3.65\%$ margin gain).
* **`area_mpc_optimizer.py` & `plot_mpc_contraction.py`**: Implements the Certainty-Equivalent Adaptive MPC outer manifold (`+82.35%` contraction margin expansion under $3.0^\circ \to 15.0^\circ$ multiplicative phase noise).
* **`run_ieee39_transients.jl` & `audit_grid_waveforms.py`**: Julia `PowerSimulationsDynamics.jl` EMT simulation and Python waveform audit pipeline for the modified IEEE 39-bus testbed.

### B. Online Mode-Shift Detection, Hysteresis & 100%-IBR Stress Tests
* **`detect_gfm_to_gfl_shift.py`**: Online Zhou–Köhler PEM-MHE estimator detecting GFM current-rail saturation and fallback into GFL mode within **$52.0\text{ ms}$**.
* **`heal_gfm_to_gfl_shift.py` & `heal_multi_device_hysteresis.py`**: Schmitt-trigger hysteresis controller (`60 ms` dwell) stabilizing simultaneous `GFM-31` mode drift and `GFL-30` $15.0^\circ$ tie-line jitter with **zero chattering** ($\lambda_{\max} \le -1.0594$).
* **`test_100pct_ibr_area.py`**: Verifies full $100\%$ IBR operation (**$0\text{ SGs}$, $7\text{ GFMs}$, $3\text{ GFLs}$**), achieving $\gamma_{\text{100ibr}}^* = 0.4018\text{ p.u.}$ (within $0.06\%$ of the legacy SG baseline) and maintaining $\lambda_{\max} \le -2.4312$ under simultaneous faults.
* **`test_gfm_reduction_threshold.py`**: Sweeps GFM anchor share from $7\text{ GFMs}$ down to $1\text{ GFM}$, proving that reducing $N_{\text{GFM}}$ from $6 \to 3$ avoids blackout ($I_{\max} = 1.0429\text{ p.u.} \le 1.20\text{ p.u.}$) and survives down to $1\text{ GFM} / 9\text{ GFL}$ ($1.1480\text{ p.u.}$).

### C. IEEE 118-Bus 3-Area Reachable Sets, MARL & Lossy Links (Paper 3)
* **`three_area_sccm_reachability.py`**:
  * Synthesizes closed-form geodesic SCCM gains across Device ($\lambda=4.50$), Area ($\lambda=2.40$), and Grid ($\lambda=1.25$) layers.
  * Computes Pontryagin reachable ellipsoids in $(V_{\text{pu}}, I_{\text{pu}})$ space ($I_{\max} = 1.0431\text{ p.u.}$).
  * Verifies Schur-complement tube containment ($\lambda_{\min} = +1041.08$ for $\mathcal{R}_{\text{Grid}} \subseteq \mathcal{R}_{\text{Area}}$, $+225.26$ for $\mathcal{R}_{\text{Area}} \subseteq \mathcal{R}_{\text{Dev}}$).
  * Exports certified PTDF thermal reserve (**$13.46\text{ MW}$** reserve / **$586.54\text{ MW}$** safe dispatch ceiling on bottleneck Line 59) directly into the 3-area IEEE 118-bus supervisory coordinator (`comm-limited-congestion-mgmt-main/`).
* **`three_area_multitimescale_bridge.py` & `compare_mit_baseline.py`**: Benchmarks the 3-tier stack against the non-communicating supervisory baseline during a $+140\text{ MW}$ Area 1 surge + parallel Line 66 trip, cutting cumulative tie-line overload from **$230.8\text{ MW}\cdot\text{s}$** ($101.3\%$ peak) to **$39.7\text{ MW}\cdot\text{s}$** ($-82.8\%$).
* **`marl_three_area_emergency.py` & `inspect_prop_delay.py`**: Evaluates isolated decentralized area agents under realistic 1-hop ($1\text{ s}$) and 2-hop ($2\text{ s}$) shadow-price propagation delays ($142.8\text{ MW}\cdot\text{s}$ overload, $-38.1\%$).
* **`test_packet_loss_resilience.py`**: Tests Zero-Order Hold (ZOH) + decay buffering under **$25\%$ random packet loss** and a **$3\text{ s}$ total link blackout**, holding cumulative overload to **$192.5\text{ MW}\cdot\text{s}$** while keeping $\lambda_{\max} \le -2.7300$.

---

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
