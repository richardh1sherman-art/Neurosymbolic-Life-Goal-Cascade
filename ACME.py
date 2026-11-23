import numpy as np

class ACMENetwork:
    def __init__(self, decay=0.1, ceiling=1.0, floor=-1.0):
        self.decay = decay
        self.max = ceiling
        self.min = floor
        
        self.nodes = []
        self.node_indices = {}
        self.activations = []
        self.weights = None
        self.pragmatic_inputs = []

    def add_node(self, name, initial_activation=0.1, pragmatic_input=0.0):
        """Adds a mapping hypothesis node to the network."""
        if name not in self.node_indices:
            self.node_indices[name] = len(self.nodes)
            self.nodes.append(name)
            self.activations.append(initial_activation)
            self.pragmatic_inputs.append(pragmatic_input)

    def initialize_weights(self):
        """Prepares the weight matrix once all nodes are added."""
        n = len(self.nodes)
        self.weights = np.zeros((n, n))
        self.activations = np.array(self.activations, dtype=float)
        self.pragmatic_inputs = np.array(self.pragmatic_inputs, dtype=float)

    def add_link(self, node_a, node_b, weight):
        """Establishes a bidirectional constraint link between two hypotheses."""
        if self.weights is None:
            self.initialize_weights()
            
        idx_a = self.node_indices[node_a]
        idx_b = self.node_indices[node_b]
        
        # ACME links are symmetric
        self.weights[idx_a, idx_b] = weight
        self.weights[idx_b, idx_a] = weight

    def update_cycle(self):
        """Runs a single discrete time-step update using the relaxation equation."""
        # Calculate net input for all nodes simultaneously: net = W * a + pragmatic
        net_inputs = np.dot(self.weights, self.activations) + self.pragmatic_inputs
        new_activations = np.copy(self.activations)

        for i in range(len(self.nodes)):
            a = self.activations[i]
            net = net_inputs[i]
            
            # ACME activation update rules
            if net > 0:
                change = net * (self.max - a) - (self.decay * a)
            else:
                change = net * (a - self.min) - (self.decay * a)
                
            new_activations[i] = np.clip(a + change, self.min, self.max)
            
        self.activations = new_activations

    def run(self, max_cycles=200, convergence_threshold=1e-4):
        """Iterates the network relaxation until equilibrium is reached."""
        if self.weights is None:
            self.initialize_weights()

        for cycle in range(max_cycles):
            old_activations = np.copy(self.activations)
            self.update_cycle()
            
            # Check for convergence (maximum absolute change among nodes)
            max_change = np.max(np.abs(self.activations - old_activations))
            if max_change < convergence_threshold:
                print(f"Network converged after {cycle + 1} cycles.")
                break
        else:
            print("Reached max cycles without full convergence.")

    def display_results(self):
        """Prints the final winning mappings sorted by activation strength."""
        print("\n--- Final Mapping Node Activations ---")
        results = sorted(zip(self.nodes, self.activations), key=lambda x: x[1], reverse=True)
        for node, act in results:
            print(f"{node:<30} : {act: .4f}")

# --- Example Setup: Solar System to Atom Mapping ---
if __name__ == "__main__":
    net = ACMENetwork(decay=0.1)

    # 1. Create mapping hypothesis nodes
    # Valid structural mappings
    net.add_node("sun=nucleus", initial_activation=0.1)
    net.add_node("planet=electron", initial_activation=0.1)
    net.add_node("attracts=attracts", initial_activation=0.1)
    
    # Competing/incorrect structural mappings
    net.add_node("sun=electron", initial_activation=0.1)
    net.add_node("planet=nucleus", initial_activation=0.1)

    # 2. Add structural support links (Excitation)
    # The relation mapping 'attracts=attracts' supports the mapping of its arguments
    net.add_link("attracts=attracts", "sun=nucleus", weight=0.1)
    net.add_link("attracts=attracts", "planet=electron", weight=0.1)

    # 3. Add one-to-one mapping constraints (Inhibition)
    # sun cannot map to both nucleus and electron
    net.add_link("sun=nucleus", "sun=electron", weight=-0.2)
    # planet cannot map to both electron and nucleus
    net.add_link("planet=electron", "planet=nucleus", weight=-0.2)
    # nucleus cannot be mapped to by both sun and planet
    net.add_link("sun=nucleus", "planet=nucleus", weight=-0.2)
    # electron cannot be mapped to by both planet and sun
    net.add_link("planet=electron", "sun=electron", weight=-0.2)

    # 4. Add a pragmatic goal boost (e.g., we care deeply about interpreting the sun)
    # We do this by feeding a small constant baseline input directly into 'sun=nucleus'
    net.node_indices["sun=nucleus"]  # Ensure it initializes correctly
    net.initialize_weights()
    net.pragmatic_inputs[net.node_indices["sun=nucleus"]] = 0.05

    # 5. Run relaxation network
    net.run()
    net.display_results()
