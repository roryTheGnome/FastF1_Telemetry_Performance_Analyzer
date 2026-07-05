import fastf1
import pandas as pd
import logging
from src.benchmarks import verify_results, run_timeit_benchmark, run_cprofile_loops, plot_benchmark
from src.session_loader import load_race_session, get_driver_telemetry
from src.telemetry_inspect import inspect_telemetry
from src.metrics import compare_drivers

fastf1.Cache.enable_cache("data")

logging.getLogger("fastf1").setLevel(logging.WARNING)

YEAR = 2026
GP = "British"
SESSION = "Q"  # Race (R) not on FastF1 yet — switch to "R" after the GP finishes
DRIVER_A = "LEC"
DRIVER_B = "HAM"
VERBOSE = False
BENCHMARK_RUNS = 50
PROFILE_RUNS = 3

def main():
    print("=" * 50)
    print("FastF1 Telemetry Performance Analyzer")
    print("=" * 50)

    session = load_race_session(YEAR, GP, SESSION)
    print(f"\nLoaded: {session.event['EventName']} — {session.name}")

    tel_a = get_driver_telemetry(session, DRIVER_A)
    tel_b = get_driver_telemetry(session, DRIVER_B)

    if VERBOSE:
        inspect_telemetry(tel_a, DRIVER_A)
        inspect_telemetry(tel_b, DRIVER_B)

    compare_drivers(session, tel_a, tel_b, DRIVER_A, DRIVER_B)

    combined = pd.concat([tel_a, tel_b], ignore_index=True)
    verify_results(combined)
    run_timeit_benchmark(combined, number=BENCHMARK_RUNS)
    run_cprofile_loops(combined, number=PROFILE_RUNS)
    plot_benchmark(combined, number=BENCHMARK_RUNS)

    print("\nDone.")


if __name__ == "__main__":
    main()