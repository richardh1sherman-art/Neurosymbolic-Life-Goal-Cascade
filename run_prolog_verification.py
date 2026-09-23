import os
import subprocess

class CompleteTriangulatedVerifier:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_forest_closure.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('exs.pl').

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: MULTI-REPRESENTATION TRIANGULATION AUDIT~n'),
    format('==================================================================================~n'),
    
    % Test Jon Barwise Channel Triangulation over Judith and the Kitchen Fire
    ( triangulated_analogy_confirmed(judith_network, kitchen_fire_network, schema_cyclic_flow_schema, schema_cyclic_flow_schema) ->
        format(' 📐 [TRIANGULATION SUCCESS]: Judith & Kitchen Fire mapped to identical channel schemas! (\u2218)~n')
    ;
        format(' ❌ Triangulation verification failed to converge.~n')
    ),
    format('==================================================================================~n'),
    halt.
"""
        os.makedirs(os.path.dirname(self.test_runner_file), exist_ok=True)
        with open(self.test_runner_file, "w", encoding="utf-8") as f:
            f.write(prolog_code)

    def execute_swipl_process(self):
        self.build_prolog_test_runner()
        result = subprocess.run(
            ["swipl", "-q", "-g", "execute_verification_audit", "verify_forest_closure.pl"],
            cwd=self.grigorchuk_dir,
            capture_output=True,
            text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    engine = CompleteTriangulatedVerifier()
    engine.execute_swipl_process()
