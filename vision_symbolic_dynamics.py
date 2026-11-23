import os
import pickle
import numpy as np

class VisualSymbolicDynamicsModel:
    """Captures spatial subshift matrices and bounding coordinates from binarized visual matrices."""
    def __init__(self, shape_name, boundaries, transition_matrix):
        self.shape_name = shape_name
        self.boundaries = boundaries  # [X_min, X_max, Y_min, Y_max]
        self.transition_matrix = transition_matrix

def parse_symbolic_geometry_from_matrix(shape_name, binary_grid):
    print(f"\n--- Extracting Symbolic Dynamics Matrix for: {shape_name} ---")
    
    # Locate index coordinates where the shape trace exists (value == 1.0)
    y_indices, x_coords = np.where(binary_grid == 1.0)
    
    if len(x_coords) == 0 or len(y_indices) == 0:
        print("   ⚠️ Empty visual matrix detected.")
        return None
        
    # Calculate the crisp topological boundaries
    x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
    y_min, y_max = int(np.min(y_indices)), int(np.max(y_indices))
    
    bounds = {"X_min": x_min, "X_max": x_max, "Y_min": y_min, "Y_max": y_max}
    print(f"   🎯 Extracted Topological Invariants: {bounds}")
    
    # Construct the subshift transition matrix:
    # Any step crossing into the shape boundary is marked as an obstruction state (0)
    shift_space_rules = {
        "inside_shape_boundary": 0,  # Blocked / Forbidden path element
        "outside_free_space": 1      # Permissible routing trajectory
    }
    
    return VisualSymbolicDynamicsModel(shape_name, bounds, shift_space_rules)

def main():
    print("=" * 95)
    print("👁️  INITIALIZING NEURO-SYMBOLIC VISION ENGINE: SHIFT TRANSITION EXTRACTOR")
    print("=" * 95)

    # Simulate an idealized binarized 30x30 square image matrix matching your pipeline resolution
    square_grid = np.zeros((30, 30))
    square_grid[10:20, 10:20] = 1.0  # Inject a solid 10x10 square shape core

    # Simulate an idealized binarized 30x30 rectangle image matrix
    rectangle_grid = np.zeros((30, 30))
    rectangle_grid[5:25, 8:22] = 1.0  # Inject a solid rectangle shape core

    # Parse both structures
    square_model = parse_symbolic_geometry_from_matrix("1_square", square_grid)
    rectangle_model = parse_symbolic_geometry_from_matrix("2_rectangle", rectangle_grid)

    # Freeze the compiled vision models directly to your pickled repository registry
    model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/story_intake_directory/pickled_models"
    os.makedirs(model_dir, exist_ok=True)
    
    payload = {"square": square_model, "rectangle": rectangle_model}
    pkl_path = os.path.join(model_dir, "level2_vision.pkl")
    
    with open(pkl_path, "wb") as f:
        pickle.dump(payload, f)
        
    print("-" * 95)
    print(f"💾 [VISION PERSISTENCE SUCCESS]: Frozen rules committed straight to -> '{os.path.basename(pkl_path)}'")
    print("   ✅ Complete discrete boundaries are now ready for Level 5 Plan Synthesis validation checking!")
    print("=" * 95 + "\n")

if __name__ == "__main__":
    main()
