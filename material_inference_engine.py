import os
import re
import subprocess

class MaterialInferenceEngine:
    """
    Implements material inferencing for the Neuro-Symbolic Self-Similar architecture.
    Applies the induced general clauses to specific context inputs to materialize
    the explicit deductive proof traces and explanation models.
    """
    def __init__(self, workspace_dir="."):
        self.workspace_dir = workspace_dir

    def materialize_explanation(self, head_name, query_args):
        """
        Runs forward-chaining material inference via a temporary Prolog sub-process
        to unpack the step-by-step state sequence and return a natural trace.
        """
        bk_path = os.path.join(self.workspace_dir, "bk.pl")
        solution_path = os.path.join(self.workspace_dir, "solution.pl")
        trace_runner = os.path.join(self.workspace_dir, "material_trace.pl")
        
        if not os.path.exists(solution_path):
            return "❌ Explanation unavailable: No induced solution rule found on disk."

        # Format a space-free compact atom statement string for the goal query
        args_str = str(query_args).replace(" ", "")
        
        # Write out an explicit Prolog tracer script using findall/3 to collect path transitions
        with open(trace_runner, "w", encoding="utf-8") as f:
            f.write(":- compile('bk.pl').\n")
            f.write(":- compile('solution.pl').\n")
            
            # Custom tracer goals tailored for Navigational vs. General Game Playing domains
            if head_name == "next_score":
                f.write(
                    f"run_trace :- \n"
                    f"    {head_name}({args_str}, Score), \n"
                    f"    findall([P, A], does({args_str.split(',')[0]}, P, A), Moves),\n"
                    f"    format('🎯 [IGGP MATERIALIZATION]: Game ID {args_str.split(',')[0]} resolved. Score output: ~w. Action parameters: ~w~n', [Score, Moves]).\n"
                )
            else:
                f.write(
                    f"run_trace :- \n"
                    f"    {head_name}({args_str.split(',')[0]}, Out), \n"
                    f"    format('🌀 [ROBOT MATERIALIZATION]: Trajectory validated. Final destination reached: ~w~n', [Out]).\n"
                )
                
        try:
            # Spawn non-blocking subprocess to capture stdout traces cleanly
            cmd = ["prolog", "-q", "-t", "halt(0)", "-g", "run_trace", "material_trace.pl"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, cwd=self.workspace_dir)
            
            if os.path.exists(trace_runner):
                os.remove(trace_runner)
                
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"⚠️ Material inference exception block fired:\n{result.stderr.strip()}"
        except Exception as e:
            if os.path.exists(trace_runner):
                os.remove(trace_runner)
            return f"❌ Subprocess initialization failure: {e}"
