import fastf1


def load_race_session(year: int, gp: str, session_type: str = "R"):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session

def get_driver_laps(session, driver: str):
    return session.laps.pick_driver(driver)

def get_driver_telemetry(session, driver: str):
    import pandas as pd

    laps = get_driver_laps(session, driver)
    chunks= []

    for _, lap in laps.iterrows():
        tel = lap.get_telemetry().add_distance()
        tel["driver"] = driver
        tel["lap"] = lap["LapNumber"]
        chunks.append(tel)

    return pd.concat(chunks, ignore_index=True)