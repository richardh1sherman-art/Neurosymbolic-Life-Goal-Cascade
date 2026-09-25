import os
import subprocess

class AlgebraicForestVerifier:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_forest_closure.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl').

verify_algebraic_closure(TargetID) :-
    ( dsl_type(variable) ->
        format(' [VALID] Algebraic Variable Types Registered in Live Architecture (\u2218).~n')
    ;
        format(' [ERROR] Variable data types missing from parser scope (\u2022).~n')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: 5TH GRADE ALGEBRAIC CLOSURE AUDIT~n'),
    format('==================================================================================~n'),
    
    verify_algebraic_closure(pencil_story), format('~n'),
    
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
    engine = AlgebraicForestVerifier()
    engine.execute_swipl_process()
