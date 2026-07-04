import numpy as np
import pandas as pd
import timeit
import cProfile
import pstats
import io
import matplotlib.pyplot as plt


def compute_pandas(df: pd.DataFrame) -> tuple[float, float, float]:
    avg_throttle = df["Throttle"].mean()
    top_speed = df["Speed"].max()
    step = df["Distance"].diff().fillna(0)
    brake_dist = step[df["Brake"]].sum()
    return avg_throttle, brake_dist, top_speed


def compute_loops(
    throttle: list[float],
    speed: list[float],
    brake: list[bool],
    distance: list[float],
) -> tuple[float, float, float]:
    n = len(throttle)
    throttle_sum = 0.0
    speed_max = speed[0]
    brake_dist = 0.0

    for i in range(n):
        throttle_sum += throttle[i]
        if speed[i] > speed_max:
            speed_max = speed[i]

    for i in range(1, n):
        if brake[i]:
            brake_dist += distance[i] - distance[i - 1]

    return throttle_sum / n, brake_dist, speed_max


def compute_numpy(
    throttle: np.ndarray,
    speed: np.ndarray,
    brake: np.ndarray,
    distance: np.ndarray,
) -> tuple[float, float, float]:
    avg_throttle = throttle.mean()
    top_speed = speed.max()
    step = np.diff(distance, prepend=distance[0])
    brake_dist = step[brake].sum()
    return float(avg_throttle), float(brake_dist), float(top_speed)


def verify_results(df: pd.DataFrame) -> None:
    pd_result = compute_pandas(df)

    throttle_l = df["Throttle"].tolist()
    speed_l = df["Speed"].tolist()
    brake_l = df["Brake"].tolist()
    distance_l = df["Distance"].tolist()
    loop_result = compute_loops(throttle_l, speed_l, brake_l, distance_l)

    throttle_a = df["Throttle"].to_numpy()
    speed_a = df["Speed"].to_numpy()
    brake_a = df["Brake"].to_numpy()
    distance_a = df["Distance"].to_numpy()
    np_result = compute_numpy(throttle_a, speed_a, brake_a, distance_a)

    names = ["avg_throttle", "brake_dist", "top_speed"]
    for name, a, b, c in zip(names, pd_result, loop_result, np_result):
        if not (abs(a - b) < 0.01 and abs(a - c) < 0.01):
            raise ValueError(f"{name}: pandas={a}, loops={b}, numpy={c}")

    print("All implementations match:")
    for name, val in zip(names, pd_result):
        print(f"  {name}: {val:.3f}")

def _prepare_arrays(df: pd.DataFrame):
    return (
        df["Throttle"].tolist(),
        df["Speed"].tolist(),
        df["Brake"].tolist(),
        df["Distance"].tolist(),
        df["Throttle"].to_numpy(),
        df["Speed"].to_numpy(),
        df["Brake"].to_numpy(),
        df["Distance"].to_numpy(),
    )


def run_timeit_benchmark(df: pd.DataFrame, number: int = 50) -> None:
    throttle_l, speed_l, brake_l, distance_l, throttle_a, speed_a, brake_a, distance_a = _prepare_arrays(df)

    pandas_time = timeit.timeit(lambda: compute_pandas(df), number=number)
    loops_time = timeit.timeit(
        lambda: compute_loops(throttle_l, speed_l, brake_l, distance_l),
        number=number,
    )
    numpy_time = timeit.timeit(
        lambda: compute_numpy(throttle_a, speed_a, brake_a, distance_a),
        number=number,
    )

    print(f"\n=== timeit ({number} runs, {len(df):,} rows) ===")
    print(f"pandas:  {pandas_time:.4f}s  ({pandas_time / number * 1000:.2f} ms/run)")
    print(f"loops:   {loops_time:.4f}s  ({loops_time / number * 1000:.2f} ms/run)")
    print(f"numpy:   {numpy_time:.4f}s  ({numpy_time / number * 1000:.2f} ms/run)")
    print(f"\nloops vs numpy: {loops_time / numpy_time:.1f}x slower")
    print(f"loops vs pandas: {loops_time / pandas_time:.1f}x slower")


def run_cprofile_loops(df: pd.DataFrame, number: int = 3) -> None:
    throttle_l, speed_l, brake_l, distance_l, *_ = _prepare_arrays(df)

    def target():
        for _ in range(number):
            compute_loops(throttle_l, speed_l, brake_l, distance_l)

    profiler = cProfile.Profile()
    profiler.enable()
    target()
    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
    stats.print_stats(15)

    print(f"\n=== cProfile (loops, {number} runs) ===")
    print(stream.getvalue())

def _bench_times(df: pd.DataFrame, number: int = 50) -> tuple[float, float, float]:
    throttle_l, speed_l, brake_l, distance_l, throttle_a, speed_a, brake_a, distance_a = _prepare_arrays(df)
    pandas_time = timeit.timeit(lambda: compute_pandas(df), number=number)
    loops_time = timeit.timeit(
        lambda: compute_loops(throttle_l, speed_l, brake_l, distance_l), number=number
    )
    numpy_time = timeit.timeit(
        lambda: compute_numpy(throttle_a, speed_a, brake_a, distance_a), number=number
    )
    return pandas_time, loops_time, numpy_time

def plot_benchmark(df: pd.DataFrame, number: int = 50, path: str = "benchmark.png") -> None:
    pandas_time, loops_time, numpy_time = _bench_times(df, number)
    plt.bar(["pandas", "loops", "numpy"], [pandas_time, loops_time, numpy_time])
    plt.ylabel("seconds")
    plt.title(f"Telemetry metrics ({len(df):,} rows, {number} runs)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"Saved {path}")
