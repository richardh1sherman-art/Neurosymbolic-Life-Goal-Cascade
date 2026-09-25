import os
import pickle
import re

class LispInterpreterEngine:
    def __init__(self):
        # 📋 Initialize a mock environmental sensor block simulating current game states
        self.game_sensors = {
            "has_higher_offer": True,
            "wave_height": 4.2,          # 🌊 Storm active over the river!
            "charged_extinguisher": False, # 🚨 Extinguisher is dead!
            "famine": True,
            "distance_to_goal": 1.2
        }

    def tokenize(self, code_string):
        """Converts raw S-expressions into standard nested Python lists."""
        # Add spacing around parentheses to split easily
        spaced = code_string.replace('(', ' ( ').replace(')', ' ) ')
        return [t for t in spaced.split() if t.strip()]

    def parse_tokens(self, tokens):
        """Recursively structures tokens into an evaluation tree lattice."""
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF while reading LISP structure.")
        
        token = tokens.pop(0)
        if token == '(':
            sub_list = []
            while tokens and tokens[0] != ')':
                sub_list.append(self.parse_tokens(tokens))
            if tokens and tokens[0] == ')':
                tokens.pop(0) # Pop off matching closing bracket
            return sub_list
        elif token == ')':
            raise SyntaxError("Unexpected closing parenthesis encountered.")
        else:
            return self.atomize(token)

    def atomize(self, token):
        """Converts raw characters into strings, booleans, or floats natively."""
        if token.lower() == 'true': return True
        if token.lower() == 'false': return False
        try:
            return float(token)
        except ValueError:
            return str(token)

    def evaluate(self, exp):
        """👑 THE RECURSIVE EVALUATION MONAD: Executes the code statements."""
        if not isinstance(exp, list):
            # If it's a raw identifier, check if it matches an environmental sensor
            if exp in self.game_sensors:
                return self.game_sensors[exp]
            return exp

        if not exp:
            return None

        operator = exp[0]
        
        # 📜 Control Flow: (if condition true_clause false_clause)
        if operator == 'if' and len(exp) >= 4:
            condition = self.evaluate(exp[1])
            if condition:
                return self.evaluate(exp[2])
            else:
                return self.evaluate(exp[3])

        # 📊 Arithmetic and Comparison Operators
        elif operator == '<' and len(exp) >= 3:
            return self.evaluate(exp[1]) < self.evaluate(exp[2])
        elif operator == 'gt' and len(exp) >= 3:
            return self.evaluate(exp[1]) > self.evaluate(exp[2])
        elif operator == 'eq' or operator == '==':
            if len(exp) >= 3:
                return self.evaluate(exp[1]) == self.evaluate(exp[2])
            return False
        elif operator == 'not' and len(exp) >= 2:
            return not self.evaluate(exp[1])

        # 🧭 Default Fallback for Action Functions (go, goto, etc.)
        else:
            evaluated_args = [self.evaluate(arg) for arg in exp[1:]]
            return f"({operator} " + " ".join(map(str, evaluated_args)) + ")"

    def run_interpreter_tests(self):
        print("=" * 95)
        print("🌀 LIVE LISP S-EXPRESSION INTERPRETER CORE DIAGNOSTICS")
        print("=" * 95)
        
        # Evaluates the actual LISP syntax blocks from your problem stories
        problems = [
            {
                "name": "Corporate Negotiation Track",
                "code": "(if has_higher_offer (goto counter_bid) (go search_maze))"
            },
            {
                "name": "Emergency Logistics Relay (Drone/Storm)",
                "code": "(if (gt wave_height 3.0) (go proceed_on_foot) (goto helicopter_flight))"
            },
            {
                "name": "Kitchen Fire Extension (Dead Extinguisher)",
                "code": "(if (not charged_extinguisher) (go evacuation_jacket) (goto use_extinguisher))"
            },
            {
                "name": "The Sovereign Household Economy",
                "code": "(if (eq famine true) (goto distribute_rations) (goto surprise_watermelon))"
            }
        ]

        for p in problems:
            print(f"📥 Context Domain ──➔ {p['name']}")
            print(f"   ├── Raw S-Expression ──➔ {p['code']}")
            
            try:
                tokens = self.tokenize(p['code'])
                parsed_ast = self.parse_tokens(tokens)
                runtime_output = self.evaluate(parsed_ast)
                print(f"   └── INTERPRETER EVALUATION OUTPUT ──➔ \033[1;32m{runtime_output}\033[0m\n")
            except Exception as e:
                print(f"   └── \033[1;31mRuntime Error: {str(e)}\033[0m\n")

        print("=" * 95)

if __name__ == "__main__":
    # 🚨 STRUCTURAL REPAIR: Safeguard parent directories against missing folder faults
    root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
    exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
    os.makedirs(os.path.dirname(exs_path), exist_ok=True)
    
    with open(exs_path, "w", encoding="utf-8") as f:
        f.write("synthesis_status(corporate_negotiation, schema_valid_non_fallacious_policy).\n")
        f.write("synthesis_status(emergency_logistics, schema_graph_minor_detour_policy).\n")
        f.write("synthesis_status(kitchen_fire_extension, schema_graph_minor_detour_policy).\n")
        f.write("synthesis_status(sovereign_economy, schema_graph_minor_detour_policy).\n")
        f.write("synthesis_status(banned_negation, schema_discarded_pruned_expression).\n")
        f.write("synthesis_status(banned_alignment, schema_discarded_pruned_expression).\n")

    engine = LispInterpreterEngine()
    engine.run_interpreter_tests()
