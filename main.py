import fastf1
import pandas as pd
from src.benchmarks import verify_results
from src.session_loader import load_race_session, get_driver_telemetry
from src.inspect import inspect_telemetry
from src.metrics import compare_drivers

fastf1.Cache.enable_cache("data")

'''CHANGE DRIVERS HERE'''
DRIVER_A = "VER"
DRIVER_B = "LEC"

if __name__ == "__main__":
    session = load_race_session(2025, "Monaco", "R")

    tel_a = get_driver_telemetry(session, DRIVER_A)
    tel_b = get_driver_telemetry(session, DRIVER_B)

    inspect_telemetry(tel_a, DRIVER_A)
    inspect_telemetry(tel_b, DRIVER_B)

    compare_drivers(session, tel_a, tel_b, DRIVER_A, DRIVER_B)

    combined = pd.concat([tel_a, tel_b], ignore_index=True)
    verify_results(combined)

    print(f"\nCombined rows for benchmarking later: {len(tel_a) + len(tel_b):,}")