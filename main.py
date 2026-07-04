import fastf1
from src.session_loader import load_race_session

fastf1.Cache.enable_cache("data")

if __name__ == "__main__":
    session = load_race_session(2025, "Monace", "R")

    print(f"Event: {session.event['EventName']}")
    print(f"Session: {session.name}")
    print(f"Drivers: {session.results['Abbreviation'].tolist()}")
    print(f"Laps loaded: {len(session.laps)}")
