import os
import json
import matplotlib
matplotlib.use('Agg')  # Guard for headless execution on DGX
import matplotlib.pyplot as plt

# Output directory configuration
output_dir = "geometric_analogy_dataset"
os.makedirs(f"{output_dir}/images", exist_ok=True)
os.makedirs(f"{output_dir}/symbolic", exist_ok=True)

def save_sample(name, fig, ax, predicates):
    """Helper function to cleanly wipe axes and save paired samples."""
    ax.axis("off")
    ax.set_xlim(-10, 110)
    ax.set_ylim(-10, 110)
    ax.set_aspect('equal')
    
    img_path = f"{output_dir}/images/{name}.png"
    json_path = f"{output_dir}/symbolic/{name}.json"
    
    plt.savefig(img_path, bbox_inches="tight", pad_inches=0.1, dpi=100)
    plt.close(fig)
    
    with open(json_path, "w") as f:
        json.dump({"sample_name": name, "predicates": predicates}, f, indent=2)

# ==========================================
# PHASE 1: SEPARATE PRIMITIVE SHAPES
# ==========================================

# 1. Standalone Square
fig, ax = plt.subplots(figsize=(4, 4))
ax.add_patch(plt.Rectangle((25, 25), 50, 50, fill=False, edgecolor="black", linewidth=3))
save_sample("1_square", fig, ax, ["shape(s1)", "type(s1, square)"])

# 2. Standalone Rectangle
fig, ax = plt.subplots(figsize=(4, 4))
ax.add_patch(plt.Rectangle((15, 35), 70, 30, fill=False, edgecolor="black", linewidth=3))
save_sample("2_rectangle", fig, ax, ["shape(r1)", "type(r1, rectangle)"])

# 3. Standalone Triangle
fig, ax = plt.subplots(figsize=(4, 4))
ax.plot([50, 20, 80, 50], [80, 20, 20, 80], color="black", linewidth=3)
save_sample("3_triangle", fig, ax, ["shape(t1)", "type(t1, triangle)"])

# 4. Standalone Circle
fig, ax = plt.subplots(figsize=(4, 4))
ax.add_patch(plt.Circle((50, 50), 30, fill=False, edgecolor="black", linewidth=3))
save_sample("4_circle", fig, ax, ["shape(c1)", "type(c1, circle)"])

# ==========================================
# PHASE 2: NESTED GEOMETRIC STRUCTURES
# ==========================================

# 5. Square Inside a Square
fig, ax = plt.subplots(figsize=(4, 4))
ax.add_patch(plt.Rectangle((20, 20), 60, 60, fill=False, edgecolor="black", linewidth=3))
ax.add_patch(plt.Rectangle((35, 35), 30, 30, fill=False, edgecolor="black", linewidth=3))
save_sample("5_square_in_square", fig, ax, [
    "shape(s_outer)", "type(s_outer, square)",
    "shape(s_inner)", "type(s_inner, square)",
    "inside(s_inner, s_outer)"
])

# 6. Triangle Inside a Circle
fig, ax = plt.subplots(figsize=(4, 4))
ax.add_patch(plt.Circle((50, 50), 35, fill=False, edgecolor="black", linewidth=3))
ax.plot([50, 20, 80, 50], [85, 32, 32, 85], color="black", linewidth=3) # Roughly inscribed
save_sample("6_triangle_in_circle", fig, ax, [
    "shape(c_outer)", "type(c_outer, circle)",
    "shape(t_inner)", "type(t_inner, triangle)",
    "inside(t_inner, c_outer)"
])

# ==========================================
# PHASE 3: 2X2 GEOMETRIC ANALOGY MATRIX
# ==========================================

# 7. Full Analogy Multi-Panel Layout
fig, ax = plt.subplots(figsize=(6, 6))

# Draw the cross dividers to divide the canvas into 4 quadrants
ax.plot([50, 50], [0, 100], color="gray", linestyle="--", linewidth=1)
ax.plot([0, 100], [50, 50], color="gray", linestyle="--", linewidth=1)

# Top Left Quadrant (Panel 1): Square inside a Square
ax.text(5, 90, "1", fontsize=14, fontweight="bold")
ax.add_patch(plt.Rectangle((12, 62), 26, 26, fill=False, edgecolor="black", linewidth=2.5))
ax.add_patch(plt.Rectangle((18, 68), 14, 14, fill=False, edgecolor="black", linewidth=2.5))

# Top Right Quadrant (Panel 2): Standalone Rectangle to the Right
ax.add_patch(plt.Rectangle((60, 67), 30, 16, fill=False, edgecolor="black", linewidth=2.5))

# Bottom Left Quadrant (Panel 3): Triangle inside a Circle
ax.text(5, 40, "3", fontsize=14, fontweight="bold")
ax.add_patch(plt.Circle((25, 25), 15, fill=False, edgecolor="black", linewidth=2.5))
ax.plot([25, 12, 38, 25], [40, 17, 17, 40], color="black", linewidth=2.5)

# Bottom Right Quadrant (Panel 4): Target Analogy Resolution Variable 'X'
ax.text(72, 21, "X", fontsize=28, color="red", fontweight="black")

# Relational Analogy Logic Labels
analogy_predicates = [
    "quadrant(top_left, panel1)", "contains(panel1, square_in_square)",
    "quadrant(top_right, panel2)", "contains(panel2, rectangle)",
    "quadrant(bottom_left, panel3)", "contains(panel3, triangle_in_circle)",
    "quadrant(bottom_right, panel4)", "contains(panel4, target_variable_x)",
    "analogy_relation(panel1, panel2, transformation_rule_A)",
    "analogy_relation(panel3, panel4, transformation_rule_A)"
]

save_sample("7_analogy_matrix", fig, ax, analogy_predicates)

print(f"Compilation successful. 7 structured dataset pairs generated inside standard location: './{output_dir}/'")
