import os
import subprocess

class SWIPLVerificationEngine:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_run.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('exs.pl').

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG TOPOLOGICAL DEDUCTION RUNNER: RECOVERED CHECK PASS~n'),
    format('==================================================================================~n'),
    forall(between(0, 9, Idx), (
        atomic_list_concat(['s_', Idx], StoryID),
        ( (validate_path_minor(station, goal_vertex, StoryID) ; validate_path_minor(airport_gate, goal_vertex, StoryID)) -> 
            format('   ➔ Story [~w] ──➔ PROOF STATUS: [SUCCESS] Traversable (\u2218).~n', [StoryID])
        ;
            format('   ➔ Story [~w] ──➔ PROOF STATUS: [FAILED] Blocked (\u2022).~n', [StoryID])
        )
    )),
    halt.
"""
        os.makedirs(os.path.dirname(self.test_runner_file), exist_ok=True)
        with open(self.test_runner_file, "w", encoding="utf-8") as f: f.write(prolog_code)

    def execute_swipl_process(self):
        self.build_prolog_test_runner()
        result = subprocess.run(
            ["swipl", "-q", "-g", "execute_verification_audit", "verify_run.pl"],
            cwd=self.grigorchuk_dir, capture_output=True, text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    engine = SWIPLVerificationEngine()
    engine.execute_swipl_process()
