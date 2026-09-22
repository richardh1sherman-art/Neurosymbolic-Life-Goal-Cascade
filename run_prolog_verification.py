import os
import subprocess

class CompleteForestVerifier:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_forest_closure.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('exs.pl').

verify_situation_status(SituationID) :-
    ( situation_classification(SituationID, SchemaDecision) ->
        format(' [VALID] Situation Core Aligned | Forest Node: ~w (\u2218).', [SchemaDecision])
    ;
        write(' [ERROR] Defective Situation Signature Detected (\u2022).')
    ).

verify_analogy_status(AnalogyID) :-
    ( analogy_evaluation(AnalogyID, AnalogySchema) ->
        format(' [VALID] Analogy Homomorphism Proved | Transfer Vertex: ~w (\u2218).', [AnalogySchema])
    ;
        write(' [ERROR] Invalid or Severed Structural Analogy (\u2022).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: MULTI-REPRESENTATION FOREST CLOSURE AUDIT~n'),
    format('==================================================================================~n'),
    
    format('   ➔ Situation [st1_timeline]             ──➔ STATUS:'), verify_situation_status(st1_timeline), format('~n'),
    format('   ➔ Situation [sb_timeline_pos]          ──➔ STATUS:'), verify_situation_status(sb_timeline_pos), format('~n'),
    format('   ➔ Situation [st2_timeline_neg]         ──➔ STATUS:'), verify_situation_status(st2_timeline_neg), format('~n'),
    format('   ➔ Situation [john_reversal_timeline]   ──➔ STATUS:'), verify_situation_status(john_reversal_timeline), format('~n'),
    format('   ➔ Situation [judith_rescue_timeline]   ──➔ STATUS:'), verify_situation_status(judith_rescue_timeline), format('~n'),
    
    % Analogy Tracks
    format('   ➔ Analogy   [kitchen_fire_transfer]     ──➔ STATUS:'), verify_analogy_status(kitchen_fire_transfer), format('~n'),
    format('   ➔ Analogy   [judith_to_prodigal_transfer]──➔ STATUS:'), verify_analogy_status(judith_to_prodigal_transfer), format('~n'),
    
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
            cwd=os.path.dirname(self.test_runner_file),
            capture_output=True,
            text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    engine = CompleteForestVerifier()
    engine.execute_swipl_process()
