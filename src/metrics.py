import pandas as pd

def avg_throttle(tel: pd.DataFrame) -> float:
    return tel["Throttle"].mean()


def top_speed(tel: pd.DataFrame) -> float:
    return tel["Speed"].max()

def braking_distance(tel: pd.DataFrame) -> float:
    step = tel["Distance"].diff().fillna(0)
    return step[tel["Brake"]].sum()


def sector_times(session, driver: str) -> dict:
    laps = session.laps.pick_drivers([driver])
    fastest = laps.pick_fastest()
    return {
        "best_lap_s": fastest["LapTime"].total_seconds(),
        "sector1_s": fastest["Sector1Time"].total_seconds(),
        "sector2_s": fastest["Sector2Time"].total_seconds(),
        "sector3_s": fastest["Sector3Time"].total_seconds(),
    }

def tire_degradation(session, driver: str) -> dict:

    laps = session.laps.pick_drivers([driver])
    laps = laps[laps["LapTime"].notna()].sort_values("LapNumber")

    compound = laps["Compound"].mode().iloc[0]
    stint = laps[laps["Compound"] == compound]

    valid = stint.iloc[1:-1]
    if len(valid) < 10:
        return {"compound": compound, "degradation_s": None}

    first5 = valid.head(5)["LapTime"].dt.total_seconds().mean()
    last5 = valid.tail(5)["LapTime"].dt.total_seconds().mean()

    return {
        "compound": compound,
        "degradation_s": last5 - first5,
    }

def driver_summary(session, driver: str, tel: pd.DataFrame) -> dict:
    sectors = sector_times(session, driver)
    tires = tire_degradation(session, driver)
    return {
        "driver": driver,
        "avg_throttle_pct": avg_throttle(tel),
        "braking_distance_m": braking_distance(tel),
        "top_speed_kmh": top_speed(tel),
        **sectors,
        **tires,
    }

def compare_drivers(session, tel_a, tel_b, driver_a, driver_b):
    a = driver_summary(session, driver_a, tel_a)
    b = driver_summary(session, driver_b, tel_b)

    print(f"\n{'Metric':<22} {driver_a:>10} {driver_b:>10}")
    print("-" * 44)
    rows = [
        ("Avg throttle (%)", "avg_throttle_pct", ".1f"),
        ("Braking dist (m)", "braking_distance_m", ".1f"),
        ("Top speed (km/h)", "top_speed_kmh", ".1f"),
        ("Best lap (s)", "best_lap_s", ".3f"),
        ("Sector 1 (s)", "sector1_s", ".3f"),
        ("Sector 2 (s)", "sector2_s", ".3f"),
        ("Sector 3 (s)", "sector3_s", ".3f"),
        ("Tire deg (s)", "degradation_s", ".3f"),
    ]
    for label, key, fmt in rows:
        va = a.get(key)
        vb = b.get(key)
        if va is None or vb is None:
            continue
        print(f"{label:<22} {va:{fmt}} {vb:{fmt}}")
    print(f"\nCompound: {a['compound']} vs {b['compound']}")
