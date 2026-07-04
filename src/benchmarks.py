import numpy as np
import pandas as pd


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
