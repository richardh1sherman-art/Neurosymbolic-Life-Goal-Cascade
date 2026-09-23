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

verify_graph_status(GraphID) :-
    ( graph_structure_classification(GraphID, GraphSchema) ->
        format(' [VALID] Graph Invariant Proved | Structural Topology: ~w (\u2218).', [GraphSchema])
    ;
        write(' [ERROR] Defective Graph Signature Detected (\u2022).')
    ).

verify_fallacy_status(ExemplarID) :-
    ( argument_fallacy_classification(ExemplarID, FallacySchema) ->
        format(' [VALID] Fallacy Class Bound | Pattern Profile: ~w (\u2218).', [FallacySchema])
    ;
        write(' [ERROR] Defective Fallacy Signature Detected (\u2022).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: MULTI-REPRESENTATION TRIANGULATION AUDIT~n'),
    format('==================================================================================~n'),
    
    % Phase 1: Verification over Graph Structures
    format('   ➔ Graph     [judith_network]            ──➔ STATUS:'), verify_graph_status(judith_network), format('~n'),
    format('   ➔ Graph     [kitchen_fire_network]      ──➔ STATUS:'), verify_graph_status(kitchen_fire_network), format('~n'),
    format('   ➔ Graph     [john_transit_network]      ──➔ STATUS:'), verify_graph_status(john_transit_network), format('~n'),
    format('   ➔ Graph     [job_loss_short]            ──➔ STATUS:'), verify_graph_status(job_loss_short), format('~n'),
    
    % Phase 2: Verification over Fallacy Classes
    format('   ➔ Fallacy   [john_tree_hugger]          ──➔ STATUS:'), verify_fallacy_status(john_tree_hugger), format('~n'),
    format('   ➔ Fallacy   [louise_campaign]           ──➔ STATUS:'), verify_fallacy_status(louise_campaign), format('~n'),
    format('   ➔ Fallacy   [bible_circularity]         ──➔ STATUS:'), verify_fallacy_status(bible_circularity), format('~n'),
    format('   ➔ Fallacy   [friend_sneeze_corona]      ──➔ STATUS:'), verify_fallacy_status(friend_sneeze_corona), format('~n'),
    
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
    engine = CompleteTriangulatedVerifier()
    engine.execute_swipl_process()
