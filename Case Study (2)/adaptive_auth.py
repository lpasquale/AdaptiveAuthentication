import subprocess
import sys
import os
import re
import time
import statistics
import resource
import psutil

command = ['z3', '-smt2', '-st', '-in']

base_smt = ''
final_model = ''
z3_model = ''

best_utility = None  # last SAT utility

# Log of (round_index, requested_u, model_utility, status)
utilities_log = []
round_counter = 0


def load_base_model(path):
    global base_smt
    with open(path, 'r') as f:
        base_smt = f.read()


def do_command(utility: float):
    
    smt_input = (
        base_smt
        + f"\n(assert (> Utility {utility} ))\n"
        + "(check-sat)\n"
        + "(get-model)\n"
    )

    return subprocess.run(
        command,
        input=smt_input,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def parse_z3_number(line: str):
    
    s = line.strip()

    # Rational form: (/ n d)
    m = re.search(r'\(/\s*([\-0-9\.]+)\s+([\-0-9\.]+)\)', s)
    if m:
        n = float(m.group(1))
        d = float(m.group(2))
        if d == 0:
            return None
        return round(n / d, 3)

    # Plain float or int with optional trailing ')'
    s = s.rstrip(')')
    try:
        return float(s)
    except ValueError:
        return None


def extract_var_from_output(name: str, output: str):
    lines = output.splitlines()
    define_prefix = f"(define-fun {name} "

    for i, line in enumerate(lines):
        if line.strip().startswith(define_prefix):
            if i + 1 < len(lines):
                value_line = lines[i + 1]
                val = parse_z3_number(value_line)
                if val is not None:
                    return val
                else:
                    return None
    return None


def is_sat_for(utility: float) -> bool:
    
    global final_model, best_utility, round_counter, utilities_log

    round_counter += 1
    result = do_command(utility)

    status = None
    model_utility = None

    if 'unsat' in result.stdout:
        status = "UNSAT"
    elif 'sat' in result.stdout:
        status = "SAT"
        # extract Utility from this particular model
        model_utility = extract_var_from_output("Utility", result.stdout)
        best_utility = utility
        final_model = result.stdout
    else:
        if result.stderr.strip():
            raise RuntimeError(f"Z3 error:\n{result.stderr}")
        raise RuntimeError("Z3 returned neither 'sat' nor 'unsat'.")

    # Log the round
    utilities_log.append(
        (round_counter, round(utility, 6), model_utility, status)
    )

    # Pretty print this round
    if status == "SAT":
        print(
            f"round {round_counter}: try Utility > {utility:.6f} "
            f"-> SAT (model Utility = {model_utility})"
        )
    else:
        print(
            f"round {round_counter}: try Utility > {utility:.6f} -> UNSAT"
        )

    return status == "SAT"


def find_max_utility_binary(min_u: float = 0.0, max_u: float = 1.0, eps: float = 0.01) -> float:
    
    global best_utility, final_model

    best_utility = None
    final_model = ''

    # Make sure the problem is satisfiable at min_u
    if not is_sat_for(min_u):
        raise RuntimeError(f"Model is UNSAT even for Utility >= {min_u}. Check your constraints.")

    if is_sat_for(max_u):
        return round(max_u, 3)

    low, high = min_u, max_u

    while high - low > eps:
        mid = (low + high) / 2.0
        if is_sat_for(mid):
            # mid is feasible -> search higher
            low = mid
        else:
            # mid is not feasible -> search lower
            high = mid

    # best_utility was updated whenever SAT
    if best_utility is None:
        raise RuntimeError("Binary search finished but no SAT utility recorded.")
    return round(best_utility, 3)


def get_line_after_string(name: str):
    if not final_model:
        return f"No model has been stored yet when searching for '{name}'."

    lines = final_model.splitlines()
    define_prefix = f"(define-fun {name} "

    for i, line in enumerate(lines):
        if line.strip().startswith(define_prefix):
            if i + 1 < len(lines):
                value_line = lines[i + 1]
                val = parse_z3_number(value_line)
                if val is not None:
                    return val
                else:
                    return f"Could not parse numeric value for '{name}' from line: {value_line}"
            else:
                return f"No line after '{name}'."
    return f"'{name}' not found in the output."


# Run Time Analysis
def run_experiment_for_scenario(scenario_id: int,
                                runs: int = 20,
                                base_dir: str = "."):
    
    scenario_dir = os.path.join(base_dir, f"Scenario{scenario_id}")
    model_path = os.path.join(scenario_dir, f"model-zu-{scenario_id}.txt")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # Load SMT model 
    load_base_model(model_path)

    times = []
    mem_peaks = []
    utilities = []

    print(f"\n=== Scenario {scenario_id}: {runs} runs ===")

    proc = psutil.Process(os.getpid())

    for i in range(1, runs + 1):

        mem_before = proc.memory_info().rss

        t0 = time.perf_counter()
        best_u = find_max_utility_binary(0.2, 0.8, eps=0.01)
        t1 = time.perf_counter()

        elapsed = t1 - t0
        times.append(elapsed)
        utilities.append(best_u)

        mem_after = proc.memory_info().rss

        current_mem_mb = mem_after / (1024.0 * 1024.0)


        mem_peaks.append(current_mem_mb)

        print(
            f"  run {i:2d}: Utility={best_u:.3f}, "
            f"time={elapsed*1000:.2f} ms, "
            f"mem≈{current_mem_mb:.2f} MB"
        )

    stats = {
        "scenario": scenario_id,
        "runs": runs,
        "time_min": min(times),
        "time_avg": statistics.mean(times),
        "time_max": max(times),
        "mem_min": min(mem_peaks),
        "mem_avg": statistics.mean(mem_peaks),
        "mem_max": max(mem_peaks),
        "utility_min": min(utilities),
        "utility_avg": statistics.mean(utilities),
        "utility_max": max(utilities),
    }

    return stats


def print_summary_table(all_stats):
    
    print("\n=== Summary (averages over runs) ===")
    header = (
        "Scenario | Runs | Time_min(ms) | Time_avg(ms) | Time_max(ms) | "
        "Mem_min(MB) | Mem_avg(MB) | Mem_max(MB) | U_min | U_avg | U_max"
    )
    print(header)
    print("-" * len(header))

    for s in all_stats:
        print(
            f"{s['scenario']:8d} | "
            f"{s['runs']:4d} | "
            f"{s['time_min']*1000:11.2f} | "
            f"{s['time_avg']*1000:11.2f} | "
            f"{s['time_max']*1000:11.2f} | "
            f"{s['mem_min']:11.2f} | "
            f"{s['mem_avg']:11.2f} | "
            f"{s['mem_max']:11.2f} | "
            f"{s['utility_min']:.3f} | "
            f"{s['utility_avg']:.3f} | "
            f"{s['utility_max']:.3f}"
        )

#'''
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = sys.argv[1]  
        z3_model = os.path.join(f"Scenario{user_input}", f"model-zu-{user_input}.txt")

        load_base_model(z3_model)

        # Find max Utility in [0, 1] with precision 0.001 
        best_u = find_max_utility_binary(0.0, 1.0, eps=0.001)

        print("\n=== Search summary ===")
        for r_idx, requested_u, model_u, status in utilities_log:
            print(f"round {r_idx:2d}: requested >= {requested_u:.6f}, "
                  f"status={status}, model Utility={model_u}")

        print("\nFinal Utility (best threshold):", best_u, "\n")

        print("PinLeng:", get_line_after_string("PinLeng"))
        print("PassStr:", get_line_after_string("PassStr"))
        print("OtpLeng:", get_line_after_string("OtpLeng"))
        print("PlateLicense:", get_line_after_string("PlateLicense"))
        print("Certificate:", get_line_after_string("Certificate"))
        print("SmartCard:", get_line_after_string("SmartCard"))
        print("Token:", get_line_after_string("Token"))
        print("SignCryp:", get_line_after_string("SignCryp"))
        print("GroupSign:", get_line_after_string("GroupSign"))
        print("RingSign:", get_line_after_string("RingSign"))
        print("Iris:", get_line_after_string("Iris"))
        print("Face:", get_line_after_string("Face"))
        print("Fingerprint:", get_line_after_string("Fingerprint"))
        print("TwoFactor:", get_line_after_string("TwoFactor"))

        print("PReplayAttack:", get_line_after_string("PReplayAttack"))
        print("PImpersAttack:", get_line_after_string("PImpersAttack"))
        print("PSessionAttack:", get_line_after_string("PSessionAttack"))
        print("AssetValue:", get_line_after_string("AssetValue"))
        print("PerformancePriority:", get_line_after_string("PerformancePriority"))
        print("ConfPriority:", get_line_after_string("ConfPriority"))
        print("AuthentPriority:", get_line_after_string("AuthentPriority"))
        print("IntegPriority:", get_line_after_string("IntegPriority"))
        print("AvgIntegrity:", get_line_after_string("AvgIntegrity"))
        print("EffectPriority:", get_line_after_string("EffectPriority"))
        print("EfficPriority:", get_line_after_string("EfficPriority"))
        print("AvgPerformance:", get_line_after_string("AvgPerformance"))
        print("PerforSum:", get_line_after_string("PerforSum"))
        print("AVGSumConf:", get_line_after_string("AVGSumConf"))
        print("AvgEfficiency:", get_line_after_string("AvgEfficiency"))

        print("Security:", get_line_after_string("Security"), "\n")
        print("Confidentiality:", get_line_after_string("Confidentiality"), "\n")
        print("Integrity:", get_line_after_string("Integrity"), "\n")
        print("Authenticity:", get_line_after_string("Authenticity"), "\n")
        print("Usability:", get_line_after_string("Usability"), "\n")
        print("Effectiveness:", get_line_after_string("Effectiveness"), "\n")
        print("Efficiency:", get_line_after_string("Efficiency"), "\n")
        print("Performance:", get_line_after_string("Performance"), "\n")
        print("Total Risk:", get_line_after_string("TotalRisk"), "\n")

        print(final_model)
        
    else:
        print("Provide a command line argument (4 | 5 | 6)")
'''

if __name__ == "__main__":
    # Configure here how many runs you want per scenario
    RUNS_PER_SCENARIO = 2

    scenarios = [1,2,3]  # Healthcare scenarios
    all_stats = []

    for sid in scenarios:
        stats = run_experiment_for_scenario(sid, runs=RUNS_PER_SCENARIO)
        all_stats.append(stats)

    print_summary_table(all_stats)

'''