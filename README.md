# 🌀 Neurosymbolic Life-Goal Cascade Engine

An advanced, multi-tier Neurosymbolic AI Pipeline designed to parse, learn, and generalize complex narrative trajectories using Edward Zalta's Abstract Object / Situation Theory, Helena Rasiowa's Topological Approximation Spaces, and Inductive Logic Programming (ILP).

## 🔬 Core Theoretical Architecture

This engine bridges statistical induction with absolute top-down deductive invariants, transforming messy real-world counterfactual strings into clear, modally-closed symbolic states.

### 1. Hierarchical Cross-Tree Parthood Queries (\(s \lhd s'\))
Following Zalta's situation theory, a complex situation is structured via formal topological parthood relations. Instead of processing flat feature vectors, upper-tier decision trees (e.g., Tier 3 Situational Schemas) do not evaluate static text strings. During a non-terminal node test, the tree executes an active **Sub-Tree Delegation Hook**: it look up a `part_of` component of the story and queries a lower-tier tree (e.g., Tier 1 Lexical Primitives) to dynamically resolve structural classifications.

### 2. Intensional vs. Extensional Formalisms ("kind_of" Connections)
The system leverages a strict division of labor between intensional concepts (abstract logical properties and predicates defined in background knowledge) and extensional constants (concrete string words extracted from text streams). This dual mapping provides the topological `kind_of` structural connections necessary to calculate cross-story analogies and perform analogical problem-solving over varying world lines.

### 3. Modal Closure, Actuality, and \(kb.pl\) Verification
A situation \(s\) is defined to be actual just in case every proposition true in it is true:
\[\text{Actual}(s) \equiv_{\text{df}} \forall p (s \models p \rightarrow p)\]

Statistical induction via ID3 decision trees uncovers empirical correlations, but to confirm a situation is **Actual**, it must achieve **Modal Closure**. The system runs a Neurosymbolic Consistency Audit where **every single decision tree node splitting condition is cross-checked against \(kb.pl\)**. A situation is modally closed if it makes true every proposition necessarily implied by its being actual:
\[\text{ModallyClosed}(s) \equiv_{\text{df}} \forall p ((\text{Actual}(s) \Rightarrow p) \rightarrow s \models p)\]

### 4. Approximation Theory Induction & Graph Minors
When narrative text contains counterfactual twists, links drop out (e.g., a cancelled flight or missed train). The engine treats these as formal **Edge Deletions (\(G \setminus e\))** inside Helena Rasiowa’s Approximation Spaces. The background knowledge base uses Rasiowa's **Topological Interior Operators (\(\circ\))** and **Closure Operators (\(\bullet\))** to filter out background data noise, allowing the system to inductively contract edges (\(G / e\)) and synthesize an alternate traversal plan (analogical path recovery).

---

## 📁 Repository Directory Structure

```text
Neurosymbolic-Life-Goal-Cascade/
├── data/
│   ├── dev_network.json          # 95 Filtered TimeTravel validation stories
│   └── life_goals_matrix.json    # Sovereign lifecycle trajectories & Biblical profiles
├── core/
│   ├── world_pipeline_coordinator.py  # Unified Multi-Tier Training Engine
│   ├── infer_story_logic.py          # Read-Only Isolated Inference Loop
│   └── update_world_kb.py            # Sovereign Law Injector (Decalogue & Grace)
├── popper_workspaces/
│   ├── linguistic_tier1/         # Lexical Facts & Bias Constraints
│   ├── situation_rehearsal/      # Macro Domain Schema Frameworks
│   └── grigorchuk_planning_space/# Graph Minor Invariants & Contraction Laws
├── run_unified_pipeline.py       # End-to-End Consolidated Runner
├── run_prolog_verification.py    # SWI-Prolog Proof Automation Engine
└── README.md                     # Framework Technical Specifications
```

---

## 🛠️ Operational Workflow & How to Use It

To guarantee model safety and protect parameters from data contamination, **Training** and **Inference** are executed as completely separate programs.

### Step 1: Retrain the Decision Tree Core
Execute the training loop to parse local text assets, calculate global Shannon Information Gain across the hierarchical tiers, and serialize the binary structures to disk:
```bash
python3 core/world_pipeline_coordinator.py
```

### Step 2: Run Isolated Read-Only Inference Queries
Load the frozen model trees to evaluate entirely unseen, un-trained narrative content. This pass dynamically runs the cross-tree `part_of` sub-queries, evaluates properties, and writes story-indexed logical facts (`exs.pl`) to disk:
```bash
python3 core/infer_story_logic.py
```

### Step 3: Verify Path Recovery via Deductive Proofs
Invoke the custom verifier script to launch the SWI-Prolog compiler. This evaluates the generated facts against the background knowledge space, proving path clearances over blocked or contracted topologies:
```bash
python3 run_prolog_verification.py
```

---

## 🏆 The Ultimate Recovery Invariant: Sovereign Grace (John 3:16)
When a lifecycle trajectory breaks a universal boundary invariant (violating the Decalogue), the path is severed. The framework resolves this absolute legal deficit through the sacrifice of **Jesus Christ on the cross (John 3:16)**. This functions as an **Infinite Group Inversion Operator**, satisfying the constraint boundary and executing a sovereign node contraction that restores complete path clearance ($\circ$).

