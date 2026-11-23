import glob
import os
import pandas as pd
import numpy as np
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple
import numpy as np


@dataclass
class SupervisoryDecision:
    command_accepted: bool
    reason: str
    enforced_word: str
    active_controllable_generators: Set[str]


class SupervisoryController:
    """
    Ramadge-Wonham + Hybrid Dwell-Time Supervisory Controller (S).
    Filters controllable switching commands (Sigma_c) against:
      1. Hybrid SCCM dwell-time bound: dt > ln(mu) / lambda
      2. Complementary breaker-pair mutual exclusion interlocks
      3. Causal prerequisite rules (e.g., g_bus must transfer before g_bank)
      4. Forbidden absorbing loss-of-lock ('F') pruning
    """

    def __init__(
        self,
        continuous_lambda: float = 1.85,
        worst_case_mu: float = 1.28,
        interlock_pairs: List[Tuple[str, str]] = None,
    ):
        self.lam = continuous_lambda
        self.mu = worst_case_mu
        self.tau_dwell_min = float(np.log(self.mu) / self.lam)

        # Empirical Caltech complementary pairs from DES_Supervisor mining
        self.interlock_pairs = interlock_pairs or [
            ("cb_123", "cb_128"),
            ("cb_134", "cb_135"),
            ("cb_137", "cb_138"),
            ("cb_140", "cb_142"),
            ("cb_146", "cb_147"),
        ]
        self.last_switch_time: float = -1e9
        self.blocked_log: List[Tuple[float, str, str]] = []

    def admissible_generators(
        self,
        current_word: str,
        t_sec: float,
        bus_transferred: bool = False,
    ) -> Set[str]:
        """Returns the supremal controllable generator subset Sigma_c(w, t)."""
        # Absorbing physical semigroup state 'F': only reset 'c' is admissible
        if "F" in current_word:
            return {"c"}

        # Enforce hybrid dwell-time guard: disable all switching until tau_dwell passes
        if (t_sec - self.last_switch_time) <= self.tau_dwell_min:
            return set()

        allowed = {"a", "c"}  # 'b' (cascading fault) is disabled under supervision
        if bus_transferred:
            allowed.add("g_bank")
        return allowed

    def check_breaker_interlocks(self, next_breaker_states: Dict[str, str]) -> Tuple[bool, str]:
        """Verifies no complementary pair is simultaneously closed ('NC') outside transfer."""
        for b1, b2 in self.interlock_pairs:
            if b1 in next_breaker_states and b2 in next_breaker_states:
                if next_breaker_states[b1] == "NC" and next_breaker_states[b2] == "NC":
                    return False, f"INTERLOCK VIOLATION: Both {b1} and {b2} commanded NC simultaneously."
        return True, "OK"

    def filter_command(
        self,
        t_sec: float,
        current_word: str,
        proposed_gen: str,
        next_word: str,
        next_breaker_states: Dict[str, str] = None,
        bus_transferred: bool = False,
    ) -> SupervisoryDecision:
        """Evaluates whether a proposed discrete transition is safe to execute."""
        allowed = self.admissible_generators(current_word, t_sec, bus_transferred)

        # 1. Check generator admissibility & dwell time
        if proposed_gen not in allowed:
            dt = t_sec - self.last_switch_time
            reason = (
                f"BLOCKED '{proposed_gen}': dt={dt:.4f}s <= tau_dwell={self.tau_dwell_min:.4f}s "
                f"or generator disabled (allowed={sorted(allowed)})."
            )
            self.blocked_log.append((t_sec, proposed_gen, reason))
            return SupervisoryDecision(False, reason, current_word, allowed)

        # 2. Check physical breaker-pair interlocks
        if next_breaker_states is not None:
            ok, msg = self.check_breaker_interlocks(next_breaker_states)
            if not ok:
                self.blocked_log.append((t_sec, proposed_gen, msg))
                return SupervisoryDecision(False, msg, current_word, allowed)

        # 3. Accept transition and update dwell timer
        self.last_switch_time = t_sec
        return SupervisoryDecision(True, "APPROVED", next_word, allowed)


def mine_caltech_event_automaton(
    timeseries_dir: str = "digital-twin-dataset/sample_dataset/topology/parameter_timeseries",
    cascade_window_sec: float = 3600.0,  # Group causal sequences within 1 hour
):
    files = sorted(glob.glob(os.path.join(timeseries_dir, "*_status.csv")))
    if not files:
        raise FileNotFoundError(f"No *_status.csv files found in {timeseries_dir}")

    events = []
    initial_state = {}

    for fpath in files:
        dev = os.path.basename(fpath).replace("-tbus_status.csv", "").replace("_status.csv", "")
        df = pd.read_csv(fpath)
        df["t"] = pd.to_datetime(df["t"])
        df = df.sort_values("t").reset_index(drop=True)

        # First row is baseline initial state
        initial_state[dev] = df.loc[0, "str"]
        for i in range(1, len(df)):
            prev_s = df.loc[i - 1, "str"]
            curr_s = df.loc[i, "str"]
            if curr_s != prev_s:
                events.append({
                    "t": df.loc[i, "t"],
                    "device": dev,
                    "from": prev_s,
                    "to": curr_s,
                    "event": f"{dev}:{prev_s}->{curr_s}",
                })

    ev_df = pd.DataFrame(events).sort_values("t").reset_index(drop=True)
    print(f"Loaded {len(files)} switching devices | Total discrete transitions: {len(ev_df)}\n")

    # 1. Group simultaneous or tight-cascade events into Macro-Transitions (Generators)
    ev_df["dt_prev"] = ev_df["t"].diff().dt.total_seconds().fillna(1e9)
    ev_df["cluster_id"] = (ev_df["dt_prev"] > cascade_window_sec).cumsum()

    print("=== 1. EXTRACTED CAUSAL EVENT SEQUENCES (IF Event A -> THEN Event B) ===")
    causal_rules = defaultdict(list)
    for cid, grp in ev_df.groupby("cluster_id"):
        t0 = grp["t"].iloc[0]
        print(f"\n[Sequence #{cid} @ {t0.isoformat()}]")
        seq_items = []
        for _, row in grp.iterrows():
            offset = (row["t"] - t0).total_seconds()
            print(f"  +{offset:8.1f}s | {row['event']}")
            seq_items.append((offset, row["event"]))

        # Record pairwise causal implications within sequence
        for i in range(len(seq_items) - 1):
            t_a, ev_a = seq_items[i]
            t_b, ev_b = seq_items[i + 1]
            causal_rules[(ev_a, ev_b)].append(t_b - t_a)

    # 2. Identify Complementary Involution Pairs (Self-Similar Group Z_2 Generators)
    print("\n=== 2. COMPLEMENTARY INVOLUTION PAIRS (SELF-SIMILAR GROUP GENERATORS) ===")
    devices = sorted(initial_state.keys())
    for i in range(len(devices)):
        for j in range(i + 1, len(devices)):
            d1, d2 = devices[i], devices[j]
            sub1 = ev_df[ev_df["device"] == d1].reset_index(drop=True)
            sub2 = ev_df[ev_df["device"] == d2].reset_index(drop=True)
            if len(sub1) == len(sub2) and len(sub1) > 0:
                diffs = np.abs((sub1["t"] - sub2["t"]).dt.total_seconds())
                opposite = all(
                    (sub1.loc[k, "from"] != sub2.loc[k, "from"])
                    and (sub1.loc[k, "to"] != sub2.loc[k, "to"])
                    for k in range(len(sub1))
                )
                if opposite and diffs.max() <= 30.0:
                    print(
                        f"  Involution Pair ({d1}, {d2}): {len(sub1)} coordinated swaps | "
                        f"max interlock delay = {diffs.max():.1f}s"
                    )

    # 3. Build Global Macro-State Automaton Trajectory
    print("\n=== 3. GLOBAL AUTOMATON STATE TRAJECTORY & DWELL TIMES ===")
    curr_global = initial_state.copy()
    last_t = None
    for cid, grp in ev_df.groupby("cluster_id"):
        t_start = grp["t"].iloc[0]
        dwell = (t_start - last_t).total_seconds() if last_t is not None else float("inf")
        for _, row in grp.iterrows():
            curr_global[row["device"]] = row["to"]
        state_word = "".join("1" if curr_global[d] == "NO" else "0" for d in devices)
        dwell_str = f"{dwell/3600:.2f} hrs" if np.isfinite(dwell) else "INIT"
        print(f"  Step {cid:02d} ({t_start.strftime('%Y-%m-%d %H:%M')}): Word={state_word} | Dwell={dwell_str}")
        last_t = grp["t"].iloc[-1]

    return ev_df, causal_rules


if __name__ == "__main__":
    ev_df, causal_rules = mine_caltech_event_automaton()

    print("\n=== 4. SUPERVISORY CONTROLLER ENFORCEMENT VERIFICATION ===")
    supervisor = SupervisoryController(continuous_lambda=1.85, worst_case_mu=1.28)
    print(f"  Certified Minimum Dwell Time (tau_dwell): {supervisor.tau_dwell_min:.4f} s")

    # Test A: Valid bus transfer at t = 1.00s
    d1 = supervisor.filter_command(
        t_sec=1.00,
        current_word="00",
        proposed_gen="a",
        next_word="10",
        next_breaker_states={"cb_123": "NO", "cb_128": "NC"},
    )
    print(f"  [t=1.00s] Valid bus swap ('a'):          Accepted={d1.command_accepted} | {d1.reason}")

    # Test B: Premature chattering switch at t = 1.08s (dt = 0.08s <= 0.1334s -> BLOCKED)
    d2 = supervisor.filter_command(
        t_sec=1.08,
        current_word="10",
        proposed_gen="a",
        next_word="00",
    )
    print(f"  [t=1.08s] Fast chattering swap ('a'):    Accepted={d2.command_accepted} | {d2.reason}")

    # Test C: Forbidden cascading fault generator ('b') at t = 1.50s -> BLOCKED
    d3 = supervisor.filter_command(
        t_sec=1.50,
        current_word="10",
        proposed_gen="b",
        next_word="1F",
    )
    print(f"  [t=1.50s] Cascading fault ('b'):         Accepted={d3.command_accepted} | {d3.reason}")

    # Test D: Interlock violation (cb_123 & cb_128 both NC) at t = 2.00s -> BLOCKED
    d4 = supervisor.filter_command(
        t_sec=2.00,
        current_word="10",
        proposed_gen="a",
        next_word="00",
        next_breaker_states={"cb_123": "NC", "cb_128": "NC"},
    )
    print(f"  [t=2.00s] Parallel closure interlock:    Accepted={d4.command_accepted} | {d4.reason}")

    # Test E: Synchronizing semigroup reset ('c') after dwell time at t = 2.50s -> APPROVED
    d5 = supervisor.filter_command(
        t_sec=2.50,
        current_word="10",
        proposed_gen="c",
        next_word="00",
        next_breaker_states={"cb_123": "NC", "cb_128": "NO"},
    )
    print(f"  [t=2.50s] Semigroup reset ('c'):         Accepted={d5.command_accepted} | {d5.reason}")