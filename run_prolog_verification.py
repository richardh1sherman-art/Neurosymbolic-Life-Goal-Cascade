import os
import subprocess

class ScienceInferenceVerifier:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_forest_closure.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('exs.pl').

verify_inference_closure(TargetID) :-
    ( science_inference_result(TargetID, Schema) ->
        format(' [VALID] Decoupled Inference Proved | Prescribed Policy: ~w (\u2218).', [Schema])
    ;
        format(' [ERROR] Inference results missing from fact sheet (\u2022).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: DECOUPLED INFERENCE CLOSURE AUDIT~n'),
    format('==================================================================================~n'),
    
    verify_inference_closure(inverted_pendulum_case1), format('~n'),
    
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
    engine = ScienceInferenceVerifier()
    engine.execute_swipl_process()
