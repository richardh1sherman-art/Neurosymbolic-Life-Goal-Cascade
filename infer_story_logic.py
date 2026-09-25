import os
import sys

class RecursiveStack:
    def __init__(self):
        self.nodes = []
    def push(self, state, path):
        self.nodes.append((state, path))
    def pop(self):
        return self.nodes.pop() if self.nodes else None
    def is_empty(self):
        return len(self.nodes) == 0

class SelfSimilarGroupSolver:
    def __init__(self):
        # State Vector: (Missionaries_Left, Cannibals_Left, Boat_Left)
        self.root_state = (3, 3, 1)
        self.identity_element = (0, 0, 0) # Goal state where word collapses to e
        
        # 🪐 ALGEBRAIC GENERATORS: Define the alphabet of discrete group operations
        # Each tuple represents: (Delta_M, Delta_C) to move in the boat
        self.generators = {
            "a": (0, 2),  # Permutation: Move 2 Cannibals
            "b": (0, 1),  # Failover: Move 1 Cannibal
            "c": (1, 1),  # Inversion: Move 1 Missionary, 1 Cannibal
            "d": (2, 0),  # Alternative: Move 2 Missionaries
            "e": (1, 0)   # Simple shift: Move 1 Missionary
        }

    def evaluate_group_invariant(self, state):
        """Self-similar boundary check: Verifies if a branch level violates the safety laws."""
        m, c, b = state
        if m < 0 or c < 0 or m > 3 or c > 3:
            return False # Hard Topological Block (•)
        if m > 0 and m < c:
            return False # Left bank mismatch: eaten
        rem_m, rem_c = 3 - m, 3 - c
        if rem_m > 0 and rem_m < rem_c:
            return False # Right bank mismatch: eaten
        return True

    def compute_pathfinder(self):
        print("=" * 95)
        print("🚀 EXECUTING PATH RECOVERY VIA SELF-SIMILAR GROUP AUTOMATON LOOPS")
        print("=" * 95)
        
        stack = RecursiveStack()
        stack.push(self.root_state, [self.root_state])
        
        visited = set()
        step = 1

        while not stack.is_empty():
            current, path = stack.pop()
            
            if current == self.identity_element:
                print("\n==================================================================================")
                print("🏆 AUTOMATON WORD COLLAPSED TO IDENTITY (e)! ALGEBRAIC PATH PROVED CLEAN:")
                print("==================================================================================")
                for idx, vertex in enumerate(path):
                    print(f"   ➔ Tree Level {idx:02d} | Coordinate Node: {vertex}")
                print("==================================================================================\n")
                return True

            if current in visited:
                continue
            visited.add(current)

            print(f"Step {step:02d} | Node {current} ──➔ Automaton evaluating sub-branch splits...")
            step += 1

            # The solver exhaustively tests group generator combinations down the tree levels
            for gen_name, (dm, dc) in self.generators.items():
                m, c, b = current
                
                # Apply group action transformations depending on the active tree split side
                if b == 1:
                    next_node = (m - dm, c - dc, 0)
                else:
                    next_node = (m + dm, c + dc, 1)

                # Evaluate the structural invariant safety check
                if not self.evaluate_group_invariant(next_node):
                    continue

                if next_node in path:
                    continue

                # Approved path transitions are pushed directly onto the recursion stack
                print(f"   └── \033[1;32mGenerator [{gen_name}]\033[0m ──➔ Transformed branch level to {next_node}")
                stack.push(next_node, path + [next_node])
                
        print("❌ Word Problem Error: Path blocked, group cannot resolve to identity element.")
        return False

if __name__ == "__main__":
    # Ensure directory existence before writing facts sheet to disk
    root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
    exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
    os.makedirs(os.path.dirname(exs_path), exist_ok=True)
    
    with open(exs_path, "w", encoding="utf-8") as f:
        f.write("situation_classification(river_crossing_loop, schema_self_similar_solution).\n")

    solver = SelfSimilarGroupSolver()
    solver.compute_pathfinder()
