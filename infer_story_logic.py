import os
import pickle

class AlgebraicLispInterpreter:
    def __init__(self):
        # 📋 Environmental state registers for our bidirectional commute problem
        self.game_sensors = {
            "distance_to_school": 5820,
            "morning_velocity": 4,
            "afternoon_time_minutes": 20
        }

    def tokenize(self, code_string):
        """Converts raw S-expressions into clean discrete tokens."""
        spaced = code_string.replace('(', ' ( ').replace(')', ' ) ')
        return [t for t in spaced.split() if t.strip()]

    def parse_tokens(self, tokens):
        """Recursively structures tokens into a balanced abstract syntax tree."""
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF while parsing algebraic matrix.")
        
        token = tokens.pop(0)
        if token == '(':
            sub_list = []
            while tokens and tokens[0] != ')':
                sub_list.append(self.parse_tokens(tokens))
            if tokens and tokens[0] == ')':
                tokens.pop(0) # 🚨 FIXED: Cleanly consume the matching closing bracket
            return sub_list
        elif token == ')':
            raise SyntaxError("Mismatched closing bracket layout.")
        else:
            return self.atomize(token)

    def atomize(self, token):
        """Resolves raw tokens into numeric primitives or symbolic atoms."""
        try:
            if '.' in token: return float(token)
            return int(token)
        except ValueError:
            return str(token)

    def evaluate(self, exp):
        """👑 RECURSIVE ALGEBRAIC EVALUATOR: Runs operations and maintains symbols."""
        if not isinstance(exp, list):
            if exp in self.game_sensors:
                return self.game_sensors[exp]
            return exp

        if not exp:
            return None

        # 🚨 FIXED: Correctly isolate the functional operator from the evaluation list
        operator = exp[0]
        args = exp[1:]

        # 🧮 Algebraic and Arithmetic Operators
        if operator == '*':
            return self.evaluate(args[0]) * self.evaluate(args[1])
        elif operator == '/':
            return self.evaluate(args[0]) / self.evaluate(args[1])
        elif operator == '-':
            return self.evaluate(args[0]) - self.evaluate(args[1])
        elif operator == '+':
            return self.evaluate(args[0]) + self.evaluate(args[1])
        elif operator == '==' or operator == 'eq':
            return self.evaluate(args[0]) == self.evaluate(args[1])
        else:
            evaluated_args = [self.evaluate(arg) for arg in args]
            return f"({operator} " + " ".join(map(str, evaluated_args)) + ")"

    def run_algebraic_suite(self):
        print("=" * 95)
        print("🌀 LIVE LISP ALGEBRAIC INTERPRETER & COMMUTE INVERSION SOLVER")
        print("=" * 95)

        # 📋 Phase 1: Morning Journey (Find Time)
        morning_sketch = "(/ distance_to_school morning_velocity)"
        morning_seconds = self.evaluate(self.parse_tokens(self.tokenize(morning_sketch)))
        print(f"📥 Morning Commute ──➔ Walking at 4 ft/sec.")
        print(f"   └── Calculated Time ──➔ \033[1;32m{int(morning_seconds // 60)} min and {int(morning_seconds % 60)} sec\033[0m\n")
        print("-" * 95)

        # 📋 Phase 2: Afternoon Return Journey (Invert Formula to Find Velocity)
        afternoon_sketch = "(/ distance_to_school (* afternoon_time_minutes 60))"
        return_velocity = self.evaluate(self.parse_tokens(self.tokenize(afternoon_sketch)))
        
        print(f"📥 Afternoon Commute ──➔ Coming home took 20 minutes.")
        print(f"   ├── Inverted S-Expression ──➔ {afternoon_sketch}")
        print(f"   └── Calculated Velocity   ──➔ \033[1;32m{return_velocity:.2f} ft/sec\033[0m")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
    exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
    os.makedirs(os.path.dirname(exs_path), exist_ok=True)
    with open(exs_path, "w", encoding="utf-8") as f:
        f.write("synthesis_status(commute_inversion_story, schema_bidirectional_closure).\n")

    engine = AlgebraicLispInterpreter()
    engine.run_algebraic_suite()
