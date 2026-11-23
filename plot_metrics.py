#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

# Clean scientific plotting styles
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2

# Grouping our 17 benchmarks into clean thematic clusters for scannability
categories = [
    "Prop Baselines\n(1-6)",
    "Trans Chains\n(7-12)",
    "Rasiowa Agent\n(13)",
    "First-Order\n(14)",
    "Zalta Modal\n(15)",
    "Zilber Metric\n(16)",
    "Zalta NFL\n(17)"
]

# Exact verified averages from your absolute multi-NN clean execution sweep
avg_latencies = [0.143, 0.137, 0.01, 0.001, 0.01, 0.001, 0.001]
avg_proof_steps = [8.5, 13.3, 13.0, 7.0, 13.0, 1.0, 1.0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# --- Panel 1: Execution Latency (Log Scale) ---
colors_lat = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#16a085', '#d35400']
bars1 = ax1.bar(categories, avg_latencies, color=colors_lat, edgecolor='black', alpha=0.85, width=0.45)
ax1.set_yscale('log')
ax1.set_ylim(1e-4, 10)
ax1.set_title("Unified Performance Latency Profile", fontsize=12, fontweight='bold', pad=15)
ax1.set_ylabel("Inference Runtime (Seconds, Log Scale)", fontsize=11, fontweight='bold')
ax1.set_xticklabels(categories, rotation=15, ha='right')
ax1.grid(True, which="both", linestyle="--", alpha=0.4)

for bar in bars1:
    h = bar.get_height()
    label_text = f"{h:.3f}s" if h >= 0.005 else "<0.001s"
    ax1.annotate(label_text, xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

# --- Panel 2: Proof Trail Footprint Steps ---
x_axis = np.arange(len(categories))
bars2 = ax2.bar(x_axis, avg_proof_steps, color='#16a085', edgecolor='black', alpha=0.85, width=0.45)
ax2.set_xticks(x_axis)
ax2.set_xticklabels(categories, rotation=15, ha='right')
ax2.set_title("Syntactic Proof Trajectory Footprint", fontsize=12, fontweight='bold', pad=15)
ax2.set_ylabel("Steps Count to Convergence", fontsize=11, fontweight='bold')
ax2.set_ylim(0, 65)
ax2.grid(True, linestyle="--", alpha=0.4)

for bar in bars2:
    h = bar.get_height()
    ax2.annotate(f"{h:.1f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
output_image_path = "zerovram_final_17_performance.png"
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
print(f"📊 SUCCESS: Refreshed 17-channel plot exported cleanly to: {output_image_path}")
